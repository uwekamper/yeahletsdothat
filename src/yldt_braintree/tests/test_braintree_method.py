# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest
import braintree
from decimal import Decimal
from mock import MagicMock, Mock
from django.test import TestCase, Client
from django.conf import settings

from campaigns.payment_method import get_method_by_name
from yldt_braintree.views import store_customer_id

from campaigns.tests.common import mock_request
from campaigns.tests.common import transaction_id
from campaigns.tests.common import campaign

@pytest.fixture
def braintree_method():
    payment_method = get_method_by_name('braintree')
    return payment_method

@pytest.fixture
def mock_transaction():
    transaction = Mock()
    transaction.amount = Decimal('23.42')
    return transaction

@pytest.mark.django_db
def test_pay(mock_request, braintree_method, campaign, transaction_id):
    result = braintree_method.pay(mock_request, campaign.key, transaction_id)
    assert result.url == '/pay/braintree/{}/'.format(transaction_id)


@pytest.mark.django_db
def test_verify(braintree_method, mock_transaction):
    result = store_customer_id(braintree_method, mock_transaction)
    assert result == False


