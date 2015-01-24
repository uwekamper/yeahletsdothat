from model_mommy import mommy
import pytest
from common import *

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
        header2 = dom.cssselect('h2')[0].text
        assert header == 'User Profile'
        assert header2 =='Your Bank Accounts'

        acc_list = dom.cssselect('#account-list li')
        assert len(acc_list) == 0

    @pytest.mark.django_db
    def test_manage_bitcoin_account(self, logged_in_client):
        """
        Go to the user profile and create a now account
        """
        dom = self.get_dom_by_name('manage_bankaccounts', client=logged_in_client)

    @pytest.mark.django_db
    def test_add_bitcoin_account(self, logged_in_client):
        """
        Go to the user profile and create a now account
        """
        dom = self.get_dom_by_name('add_bankaccount', client=logged_in_client)

@pytest.mark.django_db
class TestCampaigns(CommonMethods):
    """
    Tests for activity related things.
    """
    TEST_ACTIVITY_NAME = 'test activity'

    def test_user_can_create_activity(self, logged_in_client):
        """
        Test if a logged in user can create an activity.
        """
        pass
        #client = logged_in_client
        #url = reverse('new_activity')
        #response = client.post(url, data={'name': self.TEST_ACTIVITY_NAME})
        #assert response.status_code == 200

    def test_user_can_view_activity(self):
        """
        Check if a user can view the details of an activity.
        """
        TEST_CODE = 'WJLuiiI8NQWcJQ=='
        activity = mommy.make(Campaign, code=TEST_CODE)
        client = Client()
        response = client.get(reverse('activity', args=(activity.id, TEST_CODE)))
        assert response.status_code == 200
        dom = html.fromstring(response.content)
        header = dom.cssselect('h1')[0]
        assert response.status_code == 200

    def test_user_can_pledge(self):
        """
        Check if the user can pledge to be part of the activity.
        """
        activity = mommy.make(Campaign)
        client = Client()
        data = {
            'state': 0,
            'activity': activity.id
        }
        response = client.post(reverse('pledge_activity', args=(activity.id, )),
            data=data)
        assert response.status_code == 200

    def test_get_number_of_participants(self):
        """
        Check the function that returns the number of participants for an activity.
        """
        activity = mommy.make(Campaign)
        assert activity.get_number_of_participants() == 0
        transact = mommy.make(Transaction, state=Transaction.STATE_PAYMENT_CONFIRMED)
        assert activity.get_number_of_participants() == 1

    def test_pkgen(self):
        code = pkgen()
        assert len(code) == 16
