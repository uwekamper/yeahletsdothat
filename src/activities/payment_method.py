#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TODO: Blabla
"""

from __future__ import unicode_literals
from django.shortcuts import render
from activities.models import Transaction

method_registry = {}


class PaymentMethodDoesNotHaveName(Exception):
    """
    TODO: BLabla
    """
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BasePaymentMethod():
    """
    # TODO
    """
    def __init__(self):
        try:
            method_registry[self.name] = self
        except AttributeError:
            msg = '{} does not have a "name" member'.format(self.__class__)
            raise PaymentMethodDoesNotHaveName(msg)


    def step1(self, request):
        return render(request, 'yldt_braintree/step1.html', {})