#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import unicode_literals
import json
import jsonrpclib

from lxml import html
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from model_mommy import mommy

from activities import views
from activities.models import Activity, BankAccount, Transaction
from activities.payment_method import PaymentMethodDoesNotHaveName, BasePaymentMethod, method_registry


class CommonMethods():
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

        self.assertEqual(200, response.status_code)
        return html.fromstring(response.content)

    def get_json_by_name(self, name, args=(), client=None):
        """
        Returns the DOM.
        """
        if not client:
            client = Client()
        url = reverse(name, args=args)
        response = client.get(url)

        self.assertEqual(200, response.status_code)
        return json.loads(response.content)

    def get_logged_in_client(self, username=None, password=None):
        if not username: username = self.TEST_USERNAME
        if not password: password = self.TEST_PASSWORD

        client = Client()
        client.login(username=username, password=password)
        return client


class UserProfileTest(TestCase, CommonMethods):
    """
    Test the user profile functions
    """
    def setUp(self):
        self.create_user()

    def test_show_user_profile(self):
        """
        Go to the user profile and check if the accounts are shown.
        """
        dom = self.get_dom_by_name('user_profile', client=self.get_logged_in_client())
        header = dom.cssselect('h1')[0].text
        header2 = dom.cssselect('h2')[0].text
        self.assertEqual(header, 'User Profile')
        self.assertEqual(header2, 'Your Bank Accounts')

        acc_list = dom.cssselect('#account-list li')
        self.assertEqual(0, len(acc_list))

    def test_manage_bitcoin_account(self):
        """
        Go to the user profile and create a now account
        """
        dom = self.get_dom_by_name('manage_bankaccounts', client=self.get_logged_in_client())

    def test_add_bitcoin_account(self):
        """
        Go to the user profile and create a now account
        """
        dom = self.get_dom_by_name('add_bankaccount', client=self.get_logged_in_client())


class BankAccountTest(TestCase):

    TEST_DESCRIPTION = 'testaccount'

    def setUp(self):
        self.acc = mommy.make(BankAccount, description=self.TEST_DESCRIPTION)

    def test_can_create_account(self):
        self.assertIsInstance(self.acc, BankAccount)

    def test_get_unicode(self):
        self.assertEqual(str(self.acc), self.TEST_DESCRIPTION)


class ActivitiesTest(TestCase, CommonMethods):
    """
    Tests for activity related things.
    """
    TEST_ACTIVITY_NAME = 'test activity'

    def setUp(self):
        from collections import namedtuple
        settings_obj = namedtuple('settings', 'BTC_HOST BTC_PORT BTC_USER BTC_PASS')
        self.conf = settings_obj(
            BTC_HOST='localhost',
            BTC_PORT=18332,
            BTC_USER='bitcoinrpc',
            BTC_PASS='B726rKcomZz7rWVckYX2GsJfhRh7H6AfkDNrPHTByHRw'
        )

        self.user = self.create_user()

    def test_activity_creation(self):
        """
        Test if we can create an activity.
        """
        activity = mommy.make(Activity)
        self.assertIsInstance(activity, Activity)

    def test_user_can_create_activity(self):
        """
        Test if a logged in user can create an activity.
        """
        client = self.get_logged_in_client()
        url = reverse('new_activity')
        response = client.post(url, data={'name': self.TEST_ACTIVITY_NAME})
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_activity(self):
        """
        Check if a user can view the details of an activity.
        """
        activity = mommy.make(Activity)
        client = Client()
        response = client.get(reverse('activity', args=(activity.id, )))
        self.assertEqual(response.status_code, 200)
        dom = html.fromstring(response.content)
        header = dom.cssselect('h1')[0]
        self.assertEqual(header.text, activity.name)

    def test_user_can_pledge(self):
        """
        Check if the user can pledge to be part of the activity.
        """
        activity = mommy.make(Activity)
        client = Client()
        data = {
            'state': 0,
            'activity': activity.id
        }
        response = client.post(reverse('pledge_activity', args=(activity.id, )),
            data=data)
        self.assertEqual(response.status_code, 200)

    def test_get_number_of_participants(self):
        """
        Check the function that returns the number of participants for an activity.
        """
        activity = mommy.make(Activity)
        self.assertEqual(0, activity.get_number_of_participants())
        transact = mommy.make(Transaction, state=Transaction.STATE_PAYMENT_CONFIRMED)
        self.assertEqual(1, activity.get_number_of_participants())

    def test_get_rpc_address(self):
        result = views.get_rpc_address(self.conf)
        self.assertEqual(result, 'http://bitcoinrpc:B726rKcomZz7rWVckYX2GsJfhRh7H6AfkDNrPHTByHRw@localhost:18332/')

    def test_create_bitcoin_address(self):
        """
        TODO
        """
        s = jsonrpclib.Server(views.get_rpc_address(self.conf))
        before = len(s.listreceivedbyaddress(0, True))
        result = views.create_bitcoin_address()
        print('New address: {}'.format(result))
        after = len(s.listreceivedbyaddress(0, True))
        self.assertGreater(after, before)

    def test_transaction_api(self):
        """
        TODO
        """
        addr = views.create_bitcoin_address()
        t = mommy.make(Transaction, state=Transaction.STATE_PLEDGED, btc_address=addr,
            amount=0.001)
        data = self.get_json_by_name('transaction_api', args=(t.id,))
        print(data)
        self.assertEqual(Transaction.STATE_PLEDGED, data['state'])


class PaymentMethodTest(TestCase):

    def test_payment_method_without_name(self):
        """
        Creating a payment class without a 'name' member variable should raise
        an exception.
        """
        self.assertRaises(PaymentMethodDoesNotHaveName, BasePaymentMethod)

    def test_concrete_payment_method_creation(self):
        """
        Create a concrete example of a payment method.
        """
        class SuperPay(BasePaymentMethod):
            name = 'superpay'

        instance = SuperPay()
        self.assertIsInstance(instance, SuperPay)
        self.assertEqual(method_registry['superpay'], instance)
