# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest
from decimal import Decimal
from lxml import html
from mock import MagicMock, Mock
from django.test import TestCase, Client
from django.conf import settings

# from campaigns.payment_method import get_method_by_name
# from yldt_braintree.views import store_customer_id

from django.core.urlresolvers import reverse
from campaigns.commands import UnverifyPaymentCommand
from campaigns.models import Transaction

from campaigns.tests.common import mock_request
from campaigns.tests.common import transaction_id
from campaigns.tests.common import perk_id
from campaigns.tests.common import campaign
from campaigns.tests.common import client
from campaigns.tests.test_transactions import transaction_pledged

from yldt_braintree.views import create_customer
from yldt_braintree.views import store_verification_result
from yldt_braintree.models import BrainTreeTransaction

@pytest.fixture
def transaction_braintree_selected(transaction_id, transaction_pledged):
    UnverifyPaymentCommand(transaction_id, 'braintree')
    return Transaction.objects.get(pk=transaction_pledged.id)

@pytest.mark.django_db
def test_payment_form(client, campaign, transaction_id, transaction_braintree_selected):
    """
    Test if we can display the payment form (credit card number form) for braintree.
    """
    url = '/pay/{}/{}/'.format('braintree', transaction_id)
    resp = client.get(url)
    assert resp.status_code == 200
    dom = html.fromstring(resp.content)

    # title must be there
    page_title = dom.cssselect('title')[0].text
    assert page_title == 'Pay with Braintree'

@pytest.mark.django_db
def test_create_customer(mock_request, transaction_id, transaction_braintree_selected):
    """
    Test the subroutine that creates the Costumer object in Braintree's database.
    """
    # see https://developers.braintreepayments.com/reference/general/testing/python
    # for other possible fake testing nonces.
    result = create_customer(mock_request, transaction_braintree_selected,
        'fake-valid-visa-nonce')
    assert result.is_success == True

    #
    result_fail = create_customer(mock_request, transaction_braintree_selected,
        'fake-processor-declined-visa-nonce')
    assert result_fail.is_success == False

@pytest.mark.django_db
def test_store_verification_result(mock_request, transaction_id, transaction_braintree_selected):
    FAKE_CUST_ID = '1234567890'
    mock_success = MagicMock()
    mock_success.is_success = True
    mock_success.customer.id = FAKE_CUST_ID

    store_verification_result(transaction_id, mock_success)

    bt = BrainTreeTransaction.objects.get(transaction_id=transaction_id)
    assert bt.braintree_customer_id == FAKE_CUST_ID

