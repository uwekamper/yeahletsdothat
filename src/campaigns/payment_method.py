# -*- coding: utf-8 -*-

"""
This module contains the base class for every payment method plugin.
"""

from __future__ import unicode_literals
from django.conf import settings
from decimal import Decimal

from .utils import import_payment_method_class


# TODO: Remove the registry, probably don't need it anyway
method_registry = {}

#
# def get_actions(transaction_id):
#     """
#
#     """
#     try:
#         transaction = Transaction.objects.get(transaction_id=transaction_id)
#         return get_actions_by_name(payment_method_name, transaction_id)
#     except Transaction.DoesNotExist:
#         return []
#     except PaymentMethodDoesNotExist:
#         return []

def get_method_by_name(name):
    """
    Returns a PaymentMethod instance for the payment method with the given
    name and returns None if the
    """
    for payment_plugin in settings.YLDT_PAYMENT_METHODS:
        method_name = payment_plugin['name']
        if method_name == name:
            Klass = import_payment_method_class(payment_plugin['module_name'])
            return Klass(payment_plugin)

    # This means someone is trying to access a method that does not work.
    raise PaymentMethodDoesNotExist


def get_module_name_by_name(name):
    for payment_plugin in settings.YLDT_PAYMENT_METHODS:
        method_name = payment_plugin['name']
        if method_name == name:
            return payment_plugin['module_name']


def get_actions_by_name(name, transaction_id):
    method = get_method_by_name(name)
    return method.get_actions(transaction_id)

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


class PaymentMethodDoesNotExist(PaymentException):
    pass


class PaymentVerificationError(PaymentException):
    pass


class BasePaymentMethod(object):
    """
    Basal payment method, contains the things that are common to all
    payment methods.
    """
    def __init__(self, options):
        try:
            self.name = options['name']
            self.fee_per_transaction = options.get('fee_per_transaction', Decimal(0))
            self.fee_percent = options.get('fee_percent', Decimal(0))
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

    def get_transaction(self, transaction_id):
        pass

    def calculate_fee(self, amount):
        """
        This method shall return the payment fee that is added on top.
        """
        return (amount / Decimal(100)) * self.fee_percent + self.fee_per_transaction

    def has_fees(self):
        """
        Returns true if fees apply for this payment method.
        """
        fee = self.calculate_fee(Decimal(100))
        if fee > Decimal(0):
            return True
        else:
            return False

    def pay(self, request, campaign_key, transaction_id):
        """
        Base payment method. We will call this method whenever a payment transaction
        is created.

        Should return a valid HttpResponse instance (e.g. HttpResponseRedirect).
        """
        raise NotImplementedError()

    def unverify(self, transaction_id):
        """
        Base payment method. We will call this method whenever a payment transaction
        is inverifed.
        """
        raise NotImplementedError()

    def verify(self, request, transaction_id):
        """
        Verify a transaction. Returns True if the verification went through.
        Raises a PaymentVerificationError if there was a problem verifying the transaction.
        """
        raise NotImplementedError()

    def complete(self, campaign_key, transaction_id):
        """
        This method should be called, when the payment was successfully processed.
        It will set the transaction to STATE_PAYMENT_CONFIRMED and send an e-mail to
        the person who payed for the transaction.
        """
        pass

    def charge(self, transaction_id):
        """
        This method is called whenever we want to try to charge the customer's account.
        """
        raise NotImplementedError()

    def refund(self, campaign_key, transaction_id):
        """
        Base payment method. We will call this method whenever a payment transaction
        is created.
        """
        raise NotImplementedError()

    def get_actions(self, transaction_id=None):
        """
        Actions are displayed as buttons next to a transaction in the administrative interface.
        Using these actions administrative users can e.g. cancel a transaction manually.
        An action is a tuple that consists of a (localized) string and a URL that points to a
        view that facilitates the action.

        Example:
            [ ('Delete', '/example_payment/transactions/{}/delete/'.format(transaction_id)) ]
        """
        return []


    @property
    def module_name(self):
        return get_module_name_by_name(self.name)

    def get_json(self):
        return {'nothing_to_see_here': 'please go on'}
