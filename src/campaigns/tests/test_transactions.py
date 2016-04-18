# -*- coding: utf-8 -*-

import pytest
from decimal import Decimal
from django.utils.timezone import now, timedelta

from campaigns.models import *
from campaigns.commands import CommandError
from campaigns.commands import PledgePaymentCommand
from campaigns.commands import UnverifyPaymentCommand
from campaigns.commands import VerifyPaymentCommand
from campaigns.commands import ProcessPaymentCommand
from campaigns.commands import ReceivePaymentCommand
from campaigns.commands import AbortPaymentCommand
from campaigns.commands import RejectPaymentAttemptCommand
from .common import campaign, transaction_id, mock_request, perk_id

"""
Check if everything connected to events and event sourcing (projections,
denormalization, etc.) works as intended.
"""

@pytest.fixture
def transaction_pledged(campaign, transaction_id, perk_id):
    PledgePaymentCommand(transaction_id, campaign.key, '23.0', 'test@example.com', perk_id,
            'Henner Piffendeckel', True, 'braintree')
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    return transaction


@pytest.mark.django_db
class TestPledgedState(object):
    """
    Test the PledgePaymentCommand and the AbortPaymentCommand in the "pledged" state.
    """
    def test_pledge_payment(self, transaction_pledged):
        t = transaction_pledged
        assert t.amount == 23.0
        assert t.state == Transaction.STATE_PLEDGED
        assert t.email == 'test@example.com'

    def test_pledged_then_aborted(self, transaction_pledged, transaction_id):
        AbortPaymentCommand(transaction_id)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_ABORTED
        assert t.email == 'test@example.com'


@pytest.fixture
def transaction_unverified(transaction_id, transaction_pledged):
    UnverifyPaymentCommand(transaction_id)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    return transaction


@pytest.mark.django_db
class TestUnverifiedState(object):
    """
    Check if the transaction changes in to the "verified" state when the VerifyPaymentCommand is
    issued and if the AbortPayment command works in the "verified" state.
    """
    def test_unverify_payment(self, transaction_unverified, transaction_id):
        t = transaction_unverified
        assert t.state == Transaction.STATE_UNVERIFIED


@pytest.fixture
def transaction_verified(transaction_id, transaction_unverified):
    VerifyPaymentCommand(transaction_id)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    return transaction


@pytest.mark.django_db
class TestVerifiedState(object):
    """
    Check if we can verify a payment.
    """
    def test_verify_payment(self, transaction_verified, transaction_id):
        t = transaction_verified
        assert t.state == Transaction.STATE_VERIFIED

    def test_partially_paid(self, transaction_verified, transaction_id, mock_request):
        ReceivePaymentCommand(transaction_id, '11.5', mock_request)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_VERIFIED
        assert t.amount_received == Decimal('11.5')


@pytest.fixture
def transaction_processing(transaction_id, transaction_verified):
    ProcessPaymentCommand(transaction_id)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    return transaction


@pytest.mark.django_db
class TestProcessingState(object):
    """
    Check if we can process a payment.
    """
    def test_process_payment(self, transaction_processing, transaction_id):
        assert transaction_processing.state == Transaction.STATE_PROCESSING

    def test_payment_rejected(self, transaction_processing, transaction_id):
        t_before = transaction_processing
        assert t_before.times_rejected == 0

        # The retry count should increase every time the user tries to deduct the amount
        RejectPaymentAttemptCommand(transaction_id)
        t_after = Transaction.objects.get(transaction_id=transaction_id)
        assert t_after.state == Transaction.STATE_PROCESSING
        assert t_after.times_rejected == 1
        assert t_after.last_rejected - now() <= timedelta(seconds=2)


@pytest.fixture
def transaction_complete(transaction_id, transaction_processing, mock_request):
    ReceivePaymentCommand(transaction_id, 23.0, mock_request)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    return transaction


@pytest.mark.django_db
class TestCompleteState(object):
    """
    Check that we can complete a pay
    """
    def test_complete_payment(self, transaction_complete, transaction_id):
        t = transaction_complete
        assert t.state == Transaction.STATE_COMPLETE

    def test_abort_payment(self, transaction_complete, transaction_id):
        """
        Check that complete transaction cannot be aborted
        """
        with pytest.raises(CommandError):
            AbortPaymentCommand(transaction_id)
