# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import pytest
import json
from decimal import Decimal
from lxml import html
from django.core.urlresolvers import reverse

from campaigns.utils import get_payment_methods
from .common import client
from .common import campaign

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
    assert resp.status_code == 200






