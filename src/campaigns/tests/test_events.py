# -*- coding: utf-8 -*-

from model_mommy import mommy
import pytest
from campaigns.projectors import TransactionProjector
from common import *
import uuid
from django.utils import timezone
from campaigns.models import *
pytestmark = pytest.mark.django_db

from campaigns.commands import begin_payment, receive_payment, abort_payment

"""
Check if everything connected to events and event sourcing (projections,
denormalization, etc.) works as intended.
"""

class TestTransactionCommands(object):
    """

    """
    @pytest.fixture
    def transaction_id(self):
        return 'e3ac5128-a8d3-11e4-9f5f-002332c62ffc'

    @pytest.fixture
    def campaign(self):
        campaign = Campaign.objects.create(title='TestCampaign', currency=0,
            goal='20.0', start_date=timezone.now(), end_date=timezone.now())
        return campaign

    def test_handle_begin_payment_event(self, campaign, transaction_id):
        ev = begin_payment(transaction_id, campaign.key, 23.0, 'test@example.com')[0]
        t = TransactionState.objects.get(transaction_id=transaction_id)
        assert t.amount == 23.0
        assert t.started == ev.created
        assert t.state == TransactionState.STATE_OPEN
        assert t.email == 'test@example.com'

    def test_handle_received_payment(self, campaign, transaction_id):
        begin_payment(transaction_id, campaign.key, 23.0, 'test@example.com')

        # Send only half of the payable amount
        receive_payment(transaction_id, 11.5)
        t = TransactionState.objects.get(transaction_id=transaction_id)
        assert t.state == TransactionState.STATE_OPEN

        # Send the other half of the money
        receive_payment(transaction_id, 11.5)
        t = TransactionState.objects.get(transaction_id=transaction_id)
        assert t.state == TransactionState.STATE_COMPLETE

    def test_abort_payment(self, campaign, transaction_id):
        begin_payment(transaction_id, campaign.key, 23.0, 'test@example.com')

        # Abort the payment process
        abort_payment(transaction_id)
        t = TransactionState.objects.get(transaction_id=transaction_id)
        assert t.state == TransactionState.STATE_ABORTED