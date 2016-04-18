# -*- coding: utf-8 -*-

import json
import pytest
from decimal import Decimal
from django.test import Client
from django.core.urlresolvers import reverse
from lxml import html
from mock import Mock, MagicMock

from campaigns.models import *
from django.contrib.auth.models import User

TEST_USERNAME = 'testuser'
TEST_PASSWORD = 'test1234'
TEST_EMAIL = 'xyz@exampler.com'
TEST_CREDENTIALS = {'username': TEST_USERNAME, 'password': TEST_PASSWORD}

@pytest.fixture
def campaign():
    campaign = Campaign.objects.create(title='TestCampaign', currency=0,
        goal=Decimal(20), start_date=timezone.now(), end_date=timezone.now())
    perk = Perk.objects.create(campaign=campaign, title='TestPerk', amount=Decimal('23.0'))
    return campaign

@pytest.fixture
def perk_id(campaign):
    perk_id = campaign.perks.all()[0].id
    return perk_id

@pytest.fixture
def transaction_id():
    return 'e3ac5128-a8d3-11e4-9f5f-002332c62ffc'

@pytest.fixture
def client():
    client = Client()
    return client

def create_test_user():
    """
    Creates a user in the test database and stores it as self.user and
    also returns the User object.
    """
    username = TEST_USERNAME
    password = TEST_PASSWORD
    user = User.objects.create_user(username, TEST_EMAIL, password)
    return user

@pytest.fixture
def logged_in_client():
    client = Client()
    if not User.objects.filter(username=TEST_USERNAME).exists():
        create_test_user()
    client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
    return client

@pytest.fixture
def mock_request():
    request = Mock()
    request.build_absolute_uri = MagicMock(return_value="http://example.com/")
    return request


class CommonMethods(object):
    """
    Used as a mix-in that contains methods used by other test cases.
    """
    TEST_USERNAME = 'testuser'
    TEST_PASSWORD = 'test1234'
    TEST_EMAIL = 'xyz@exampler.com'
    TEST_CREDENTIALS = {'username': TEST_USERNAME, 'password': TEST_PASSWORD}

    def create_user(self, username=None, password=None):
        """
        Creates a user in the test database and stores it as self.user and
        also returns the User object.
        """
        if not username:
            username = self.TEST_USERNAME
        if not password:
            password = self.TEST_PASSWORD
        self.user = User.objects.create_user(username, self.TEST_EMAIL, password)
        return self.user

    def get_dom_by_name(self, name, args=(), client=None):
        """
        Returns the DOM.
        """
        if not client:
            client = Client()
        url = reverse(name, args=args)
        response = client.get(url)

        assert response.status_code == 200
        return html.fromstring(response.content)

    def get_json_by_name(self, name, args=(), client=None):
        """
        Returns the DOM.
        """
        if not client:
            client = Client()
        url = reverse(name, args=args)
        response = client.get(url)

        assert response.status_code == 200
        return json.loads(response.content)

    def get_logged_in_client(self, username=None, password=None):
        if not username: username = self.TEST_USERNAME
        if not password: password = self.TEST_PASSWORD

        client = Client()
        client.login(username=username, password=password)
        return client
