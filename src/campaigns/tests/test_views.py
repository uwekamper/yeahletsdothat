#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import unicode_literals
import json
from decimal import Decimal
import pytest
from lxml import html
from django.core.urlresolvers import reverse
from campaigns.utils import get_payment_methods
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

    # title must be there
    perk_title = dom.cssselect('#perk-title')[0].text
    assert perk_title == perk.title

    # the amount must be high enough
    dom_amount = dom.cssselect('#id_amount')[0]
    assert Decimal(dom_amount.value) >= perk.amount

@pytest.mark.django_db
def test_select_payment_with_low_amount(client, campaign):
    """
    Test if we can select a payment and a perk
    """
    method = get_payment_methods()[0]
    perk = campaign.perks.last()
    resp = client.post(
        reverse('select_payment', args=[campaign.key]) + '?perk={}'.format(perk.id),
        data={
            'payment_method': method,
            'amount': str(perk.amount / Decimal('2.0')),
            'email1': 'test@example.com',
            'email2': 'test@example.com',
        })
    assert resp.status_code == 200
    dom = html.fromstring(resp.content)

    # there should be errors
    assert len(dom.cssselect('.errorlist')) >= 1


@pytest.mark.django_db
def test_select_payment_with_right_amount(client, campaign):
    """
    Test if we can select a payment and a perk
    """
    method = get_payment_methods()[0]
    perk = campaign.perks.last()
    resp = client.post(
        reverse('select_payment', args=[campaign.key]) + '?perk={}'.format(perk.id),
        data={
            'payment_method': method.name,
            'amount': str(perk.amount),
            'email1': 'test@example.com',
            'email2': 'test@example.com',
        })
    # should redirect to a payment page.
    assert resp.status_code == 302


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





