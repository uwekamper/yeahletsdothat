#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TODO: Blabla
"""

from __future__ import unicode_literals
from django.conf import settings

# TODO: Remove the registry, probably don't need it anyway
method_registry = {}

def get_method_by_name(name):
    """
    Returns a PaymentMethod instance for the payment method with the given
    name and returns None if the
    """
    for payment_plugin in settings.YLDT_PAYMENT_METHODS:
        method_name = payment_plugin['name']
        if method_name == name:
            method = __import__(payment_plugin['module_name'])
            return method.PaymentMethod(payment_plugin)

    # This means someone is trying to access a method that does not work.
    raise PaymentMethodDoseNotExist


class PaymentException(Exception):
    """
    Base class for all payment related exceptions.
    """
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PaymentMethodDoesNotHaveName(PaymentException):
    pass

class PaymentMethodDoesNotHaveCurrencies(PaymentException):
    pass

class PaymentMethodDoseNotExist(PaymentException):
    pass


class BasePaymentMethod(object):
    """
    Basal peyment method, contains the things that are common to all
    payment methods.
    """
    def __init__(self, options):
        try:
            self.name = options['name']
            method_registry[options['name']] = self
        except KeyError:
            msg = '{} does not have a "name" member'.format(self.__class__)
            raise PaymentMethodDoesNotHaveName(msg)
        try:
            self.currencies = options['currencies']
        except KeyError:
            msg = 'You must provide a list of currencies for {}.'.format(self.__class__)
            raise PaymentMethodDoesNotHaveCurrencies(msg)

        self.display_name = options['display_name']


    def pay(self, campaign, transaction):
        """
        Base payment method. We will call this method whenever a payment transaction
        is created.

        Should return a valid HttpResponse instance (e.g. HttpResponseRedirect).
        """
        raise NotImplementedError()

    def complete(self, campaign, transaction):
        """
        This method should be called, when the payment was successfully processed.
        It will set the transaction to STATE_PAYMENT_CONFIRMED and send an e-mail to
        the person who payed for the transaction.
        """
        pass

    def refund(self, campaign, transaction):
        """
        Base payment method. We will call this method whenever a payment transaction
        is created.
        """
        raise NotImplementedError()