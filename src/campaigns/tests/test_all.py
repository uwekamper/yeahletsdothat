#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import unicode_literals
import json
import pytest
from lxml import html
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from model_mommy import mommy

from campaigns import views
from campaigns.models import Campaign, BankAccount, Transaction, pkgen
from campaigns.payment_method import PaymentMethodDoesNotHaveName, BasePaymentMethod, method_registry
from common import CommonMethods

@pytest.mark.django_db
def test_campaign_creation():
    """
    Test if we can create an activity.
    """
    campaign = mommy.make(Campaign)
    assert isinstance(campaign, Campaign)


class BankAccountTest(TestCase):

    TEST_DESCRIPTION = 'testaccount'

    def setUp(self):
        self.acc = mommy.make(BankAccount, description=self.TEST_DESCRIPTION)

    def test_can_create_account(self):
        self.assertIsInstance(self.acc, BankAccount)

    def test_get_unicode(self):
        self.assertEqual(str(self.acc), self.TEST_DESCRIPTION)





