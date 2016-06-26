#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404

from campaigns.models import Campaign

def import_payment_method_class(full_module_name):
    module_name, class_name = full_module_name.rsplit('.', 1)
    module = __import__(module_name, fromlist=[class_name, ])
    klass = getattr(module, class_name)
    return klass


def get_campaign_or_404(request, key):
    """
    Returns a Campaign object if the key is valid or raises 404.
    """
    campaign = get_object_or_404(Campaign, key=key)
    return campaign

def get_payment_methods():
    methods = []
    for options in settings.YLDT_PAYMENT_METHODS:
        klass = import_payment_method_class(options['module_name'])
        instance = klass(options=options)
        methods.append(instance)
    return methods

def get_payment_method_names():
    names = [(x.name, x.name) for x in get_payment_methods()]
    return names
