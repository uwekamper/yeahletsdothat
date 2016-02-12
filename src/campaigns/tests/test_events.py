# -*- coding: utf-8 -*-

from common import campaign, transaction_id
from campaigns.models import *
from campaigns.commands import PledgePayment, ReceivePayment, AbortPayment

"""
Check if everything connected to events and event sourcing (projections,
denormalization, etc.) works as intended.
"""

@pytest.mark.django_db
class TestTransactionCommands(object):

    @pytest.fixture
    def perk_id(self, campaign):
        perk_id = campaign.perks.all()[0].id
        return perk_id

    def test_handle_pledge_payment_event(self, campaign, transaction_id, perk_id):
        PledgePayment(transaction_id, campaign.key, 23.0, 'test@example.com', perk_id,
            'Henner Piffendeckel', True, 'braintree')
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.amount == 23.0
        assert t.state == Transaction.STATE_PLEDGED
        assert t.email == 'test@example.com'

    def test_handle_received_payment(self, campaign, transaction_id, perk_id, mock_request):
        PledgePayment(transaction_id, campaign.key, 23.0, 'test@example.com', perk_id,
            'Henner Piffendeckel', True, 'braintree')

        # Send only half of the payable amount
        ReceivePayment(transaction_id, 11.5, mock_request)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_PLEDGED

        # Send the other half of the money
        ReceivePayment(transaction_id, 11.5, mock_request)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_COMPLETE

    def test_abort_payment(self, campaign, transaction_id, perk_id):
        PledgePayment(transaction_id, campaign.key, 23.0, 'test@example.com', perk_id,
            'Henner Piffendeckel', True, 'braintree')

        # Abort the payment process
        AbortPayment(transaction_id)
        t = Transaction.objects.get(transaction_id=transaction_id)
        assert t.state == Transaction.STATE_ABORTED

    def test_campaign_state_completion(self, campaign, transaction_id, perk_id, mock_request):
        """
        Test if the campaign state goes to 'complete' if there are enough
        completed transactions.
        """
        assert campaign.state.completed == False
        assert campaign.state.total_supporters == 0

        # add one supporter

        PledgePayment(transaction_id, campaign.key, 20.0, 'test@example.com', perk_id,
            'Henner Piffendeckel', True, 'braintree')
        changed_campaign = Campaign.objects.get(id=campaign.id)
        assert changed_campaign.state.total_pledged == Decimal('20.0')
        assert changed_campaign.state.total_received == Decimal('0.0')
        assert changed_campaign.state.total_supporters == 0
        assert changed_campaign.state.total_pledgers == 1

        perk = changed_campaign.perks.all()[0]
        assert perk.state.total_pledged == 1
        assert perk.state.total_received == 0

        # Complete the payment
        ReceivePayment(transaction_id, 20.0, mock_request)

        # check everything on  the completed campaign.
        changed_campaign = Campaign.objects.get(id=campaign.id)
        assert changed_campaign.state.total_received == Decimal('20.0')
        assert changed_campaign.state.completed == True
        assert changed_campaign.state.total_supporters == 1

        perk = changed_campaign.perks.all()[0]
        assert perk.state.total_pledged == 1
        assert perk.state.total_received == 1

    def test_campaign_state_percent(self, campaign, transaction_id, perk_id, mock_request):
        """
        Check if the model shows the correct percentage
        """
        PledgePayment(transaction_id, campaign.key, Decimal(10), 'test@example.com', perk_id,
            'Testuser', True, 'braintree')
        ReceivePayment(transaction_id, Decimal(10), mock_request)
        assert campaign.state.percent_funded == Decimal(50.0)

    def test_campaign_state_pending(self, campaign, transaction_id, perk_id, mock_request):
        """
        Check if the model shows the amount of pending amounts.
        """
        PledgePayment(transaction_id, campaign.key, Decimal(10), 'test@example.com', perk_id,
            'Testuser', True, 'braintree')
        assert campaign.state.pending == Decimal(10)
        ReceivePayment(transaction_id, Decimal(10), mock_request)

        changed_campaign = Campaign.objects.get(id=campaign.id)
        assert changed_campaign.state.pending == Decimal(0)

