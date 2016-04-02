# -*- coding: utf-8 -*-

import uuid
import pytest

from decimal import Decimal
from model_mommy import mommy
from campaigns.commands import PledgePaymentCommand, ReceivePayment

from .common import *

pytestmark = pytest.mark.django_db

class TestUserProfile(CommonMethods):
    """
    Test the user profile functions
    """

    @pytest.mark.django_db
    def test_show_user_profile(self, logged_in_client):
        """
        Go to the user profile and check if the accounts are shown.
        """
        dom = self.get_dom_by_name('user_profile', client=logged_in_client)
        header = dom.cssselect('h1')[0].text
        assert header == 'User Profile'

        acc_list = dom.cssselect('#account-list li')
        assert len(acc_list) == 0

#    @pytest.mark.django_db
    # def test_manage_bitcoin_account(self, logged_in_client):
    #     """
    #     Go to the user profile and create a now account
    #     """
    #     dom = self.get_dom_by_name('manage_bankaccounts', client=logged_in_client)

    # @pytest.mark.django_db
    # def test_add_bitcoin_account(self, logged_in_client):
    #     """
    #     Go to the user profile and create a now account
    #     """
    #     dom = self.get_dom_by_name('add_bankaccount', client=logged_in_client)

@pytest.mark.django_db
class TestCampaigns(CommonMethods):
    """
    Tests for campaign related things.
    """
    TEST_ACTIVITY_NAME = 'test activity'

    def test_user_can_view_campaign(self):
        """
        Check if a user can view the details of an activity.
        """
        TEST_CODE = 'WJLuiiI8NQWcJQ=='
        campaign = mommy.make(Campaign, key=TEST_CODE)
        client = Client()
        response = client.get(reverse('campaign_details', args=[TEST_CODE]))
        assert response.status_code == 200
        dom = html.fromstring(response.content)
        header = dom.cssselect('h1')[0]
        assert response.status_code == 200

    def test_user_can_pledge(self):
        """
        Check if the user can pledge to be part of the activity.
        """
        campaign = mommy.make(Campaign)
        client = Client()

        response = client.get(reverse('select_payment', args=(campaign.key, )),)
        assert response.status_code == 200

    def test_pkgen(self):
        code = pkgen()
        assert len(code) == 16

    def test_has_started(self):
        start_date = timezone.now()
        TEST_CODE = 'WJLuiiI8NQWcJQ=='
        campaign = mommy.make(Campaign, key=TEST_CODE, start_date=timezone.now())
        assert campaign.has_started == True