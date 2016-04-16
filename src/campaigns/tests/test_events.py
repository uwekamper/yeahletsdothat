# -*- coding: utf-8 -*-

import pytest

from campaigns.models import *
from campaigns.commands import PledgePaymentCommand
from campaigns.commands import UnverifyPaymentCommand
from campaigns.commands import VerifyPaymentCommand
from campaigns.commands import ProcessPaymentCommand
from campaigns.commands import ReceivePaymentCommand
from campaigns.commands import AbortPaymentCommand
from .common import campaign, transaction_id, mock_request

"""
Check if everything connected to events and event sourcing (projections,
denormalization, etc.) works as intended.
"""
@pytest.fixture
def perk_id(campaign):
    perk_id = campaign.perks.all()[0].id
    return perk_id

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
        t = transaction_processing
        assert t.state == Transaction.STATE_PROCESSING



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

    # TODO: Check that complete transaction cannot be aborted

    ## TODO: repair this and maybe move to a better place
    # def test_handle_received_payment(self, campaign, transaction_id, perk_id, mock_request):
    #     PledgePaymentCommand(transaction_id, campaign.key, 23.0, 'test@example.com', perk_id,
    #         'Henner Piffendeckel', True, 'braintree')
    #
    #     # Send only half of the payable amount
    #     ReceivePaymentCommand(transaction_id, 11.5, mock_request)
    #     t = Transaction.objects.get(transaction_id=transaction_id)
    #     assert t.state == Transaction.STATE_PLEDGED
    #
    #     # Send the other half of the money
    #     ReceivePaymentCommand(transaction_id, 11.5, mock_request)
    #     t = Transaction.objects.get(transaction_id=transaction_id)
    #     assert t.state == Transaction.STATE_COMPLETE

    ## TODO: repair this and maybe move to a better place
    # def test_abort_payment(self, campaign, transaction_id, perk_id):
    #     PledgePaymentCommand(transaction_id, campaign.key, 23.0, 'test@example.com', perk_id,
    #         'Henner Piffendeckel', True, 'braintree')
    #
    #     # Abort the payment process
    #     AbortPaymentCommand(transaction_id)
    #     t = Transaction.objects.get(transaction_id=transaction_id)
    #     assert t.state == Transaction.STATE_ABORTED

    ## TODO: repair this and maybe move to a better place
    # def test_campaign_state_completion(self, campaign, transaction_id, perk_id, mock_request):
    #     """
    #     Test if the campaign state goes to 'complete' if there are enough
    #     completed transactions.
    #     """
    #     assert campaign.state.completed == False
    #     assert campaign.state.total_supporters == 0
    #
    #     # add one supporter
    #
    #     PledgePaymentCommand(transaction_id, campaign.key, 20.0, 'test@example.com', perk_id,
    #         'Henner Piffendeckel', True, 'braintree')
    #     changed_campaign = Campaign.objects.get(id=campaign.id)
    #     assert changed_campaign.state.total_pledged == Decimal('20.0')
    #     assert changed_campaign.state.total_received == Decimal('0.0')
    #     assert changed_campaign.state.total_supporters == 0
    #     assert changed_campaign.state.total_pledgers == 1
    #
    #     perk = changed_campaign.perks.all()[0]
    #     assert perk.state.total_pledged == 1
    #     assert perk.state.total_received == 0
    #
    #     # Complete the payment
    #     ReceivePaymentCommand(transaction_id, 20.0, mock_request)
    #
    #     # check everything on  the completed campaign.
    #     changed_campaign = Campaign.objects.get(id=campaign.id)
    #     assert changed_campaign.state.total_received == Decimal('20.0')
    #     assert changed_campaign.state.completed == True
    #     assert changed_campaign.state.total_supporters == 1
    #
    #     perk = changed_campaign.perks.all()[0]
    #     assert perk.state.total_pledged == 1
    #     assert perk.state.total_received == 1

    ## TODO: repair this and maybe move to a better place
    # def test_campaign_state_percent(self, campaign, transaction_id, perk_id, mock_request):
    #     """
    #     Check if the model shows the correct percentage
    #     """
    #     PledgePaymentCommand(transaction_id, campaign.key, Decimal(10), 'test@example.com', perk_id,
    #         'Testuser', True, 'braintree')
    #     ReceivePaymentCommand(transaction_id, Decimal(10), mock_request)
    #     assert campaign.state.percent_funded == Decimal(50.0)

    ## TODO: repair this and maybe move to a better place
    # def test_campaign_state_pending(self, campaign, transaction_id, perk_id, mock_request):
    #     """
    #     Check if the model shows the amount of pending amounts.
    #     """
    #     PledgePaymentCommand(transaction_id, campaign.key, Decimal(10), 'test@example.com', perk_id,
    #         'Testuser', True, 'braintree')
    #     assert campaign.state.pending == Decimal(10)
    #     ReceivePaymentCommand(transaction_id, Decimal(10), mock_request)
    #
    #     changed_campaign = Campaign.objects.get(id=campaign.id)
    #     assert changed_campaign.state.pending == Decimal(0)

