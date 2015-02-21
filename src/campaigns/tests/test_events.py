# -*- coding: utf-8 -*-

from common import *
from campaigns.models import *
pytestmark = pytest.mark.django_db

from campaigns.commands import begin_payment, receive_payment, abort_payment

"""
Check if everything connected to events and event sourcing (projections,
denormalization, etc.) works as intended.
"""

class TestTransactionCommands(object):

    @pytest.fixture
    def transaction_id(self):
        return 'e3ac5128-a8d3-11e4-9f5f-002332c62ffc'



    def test_handle_begin_payment_event(self, campaign, transaction_id):
        ev = begin_payment(transaction_id, campaign.key, 23.0, 'test@example.com')[0]
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.amount == 23.0
        assert t.started == ev.created
        assert t.state == Transaction.STATE_OPEN
        assert t.email == 'test@example.com'

    def test_handle_received_payment(self, campaign, transaction_id):
        begin_payment(transaction_id, campaign.key, 23.0, 'test@example.com')

        # Send only half of the payable amount
        receive_payment(transaction_id, 11.5)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_OPEN

        # Send the other half of the money
        receive_payment(transaction_id, 11.5)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_COMPLETE

    def test_abort_payment(self, campaign, transaction_id):
        begin_payment(transaction_id, campaign.key, 23.0, 'test@example.com')

        # Abort the payment process
        abort_payment(transaction_id)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_ABORTED