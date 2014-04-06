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
        method = __import__(payment_plugin)
        if method.PaymentMethod.name == name:
            return method.PaymentMethod()

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


class PaymentMethodDoseNotExist(PaymentException):
    pass


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

    def pay(self, campaign, transaction):
        """
        Base payment method. We will call this method whenever a payment transaction
        is created.
        """
        raise NotImplementedError()

