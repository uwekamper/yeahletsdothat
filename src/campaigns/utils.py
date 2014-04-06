#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404

from campaigns.models import Campaign


def get_campaign_or_404(request, key):
    """
    Returns a Campaign object if the key is valid or raises 404.
    """
    campaign = get_object_or_404(Campaign, key=key)
    return campaign

def get_payment_methods():
    methods = []
    for method_name in settings.YLDT_PAYMENT_METHODS:
        module = __import__(method_name)
        methods.append(module.PaymentMethod())
    return methods

def get_payment_method_names():
    names = [(x.name, x.name) for x in get_payment_methods()]
    return names
