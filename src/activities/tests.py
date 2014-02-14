#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from lxml import html

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from model_mommy import mommy

from activities.models import Activity


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


class ActivitiesTest(TestCase, CommonMethods):
    """
    Tests for activity related things.
    """
    TEST_ACTIVITY_NAME = 'test activity'

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
        self.create_user()
        client = Client()
        logged_in = client.login(**self.TEST_CREDENTIALS)
        self.assertTrue(logged_in)
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





