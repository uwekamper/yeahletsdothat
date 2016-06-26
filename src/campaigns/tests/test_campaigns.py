# -*- coding: utf-8 -*-

import pytest
from decimal import Decimal
from django.utils.timezone import now, timedelta

from .common import campaign
from .common import transaction_id
from .common import mock_request
from .common import perk_id
from campaigns.models import Campaign
from campaigns import commands

@pytest.mark.django_db
def test_campaign_state_percent(campaign, transaction_id, perk_id, mock_request):
    """
    Check if the model shows the correct percentage
    """
    commands.PledgePaymentCommand(transaction_id, campaign.key, Decimal(10), 'test@example.com',
        perk_id, 'Testuser', str(True))
    commands.UnverifyPaymentCommand(transaction_id, 'braintree')

    commands.ReceivePaymentCommand(transaction_id, Decimal(10), mock_request)
    assert campaign.state.percent_funded == Decimal(50.0)

@pytest.mark.django_db
def test_campaign_state_pending(campaign, transaction_id, perk_id, mock_request):
    """
    Check if the model shows the amount of pending amounts.
    """
    commands.PledgePaymentCommand(transaction_id, campaign.key, Decimal(10), 'test@example.com',
        perk_id, 'Testuser', True)
    commands.UnverifyPaymentCommand(transaction_id, 'braintree')
    commands.VerifyPaymentCommand(transaction_id)

    assert campaign.state.pending == Decimal(10)
    commands.ReceivePaymentCommand(transaction_id, Decimal(10), mock_request)

    changed_campaign = Campaign.objects.get(id=campaign.id)
    assert changed_campaign.state.pending == Decimal(0)


# TODO: repair this and maybe move to a better place
@pytest.mark.django_db
def test_campaign_state_completion(campaign, transaction_id, perk_id, mock_request):
    """
    Test if the campaign state goes to 'complete' if there are enough
    completed transactions.
    """
    assert campaign.state.completed == False
    assert campaign.state.total_supporters == 0

    commands.PledgePaymentCommand(transaction_id, campaign.key, 20.0, 'test@example.com', perk_id,
        'Henner Piffendeckel', True)
    commands.UnverifyPaymentCommand(transaction_id, 'braintree')
    commands.VerifyPaymentCommand(transaction_id)

    changed_campaign = Campaign.objects.get(id=campaign.id)
    assert changed_campaign.state.total_pledged == Decimal('20.0')
    assert changed_campaign.state.total_received == Decimal('0.0')
    assert changed_campaign.state.total_supporters == 0
    assert changed_campaign.state.total_pledgers == 1

    perk = changed_campaign.perks.all()[0]
    assert perk.state.total_pledged == 1
    assert perk.state.total_received == 0

    # Complete the payment
    commands.ReceivePaymentCommand(transaction_id, 20.0, mock_request)

    # check everything on  the completed campaign.
    changed_campaign = Campaign.objects.get(id=campaign.id)
    assert changed_campaign.state.total_received == Decimal('20.0')
    assert changed_campaign.state.completed == True
    assert changed_campaign.state.total_supporters == 1

    perk = changed_campaign.perks.all()[0]
    assert perk.state.total_pledged == 1
    assert perk.state.total_received == 1
