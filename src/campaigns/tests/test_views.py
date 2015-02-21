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
from django.core.urlresolvers import reverse
# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.test.client import Client
# from model_mommy import mommy
#
# from campaigns import views
# from campaigns.models import Campaign, BankAccount, Transaction, pkgen
# from campaigns.payment_method import PaymentMethodDoesNotHaveName, BasePaymentMethod, method_registry
# from common import CommonMethods

from common import client, campaign

@pytest.mark.django_db
def test_select_payment(client, campaign):
    """
    Test if we can select a payment and a perk
    """
    perk = campaign.perks.last()
    resp = client.get(reverse('select_payment', args=[campaign.key]) + '?perk={}'.format(perk.id))
    assert resp.status_code == 200
    dom = html.fromstring(resp.content)
    perk_title = dom.cssselect('#perk-title')[0].text
    assert perk_title == perk.title



# class BankAccountTest(TestCase):
#
#     TEST_DESCRIPTION = 'testaccount'
#
#     def setUp(self):
#         self.acc = mommy.make(BankAccount, description=self.TEST_DESCRIPTION)
#
#     def test_can_create_account(self):
#         self.assertIsInstance(self.acc, BankAccount)
#
#     def test_get_unicode(self):
#         self.assertEqual(str(self.acc), self.TEST_DESCRIPTION)





