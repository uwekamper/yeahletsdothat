# -*- coding: utf-8 -*-

import pytest
from decimal import Decimal
from campaigns.payment_method import BasePaymentMethod, PaymentMethodDoesNotHaveName, \
    PaymentMethodDoesNotHaveCurrencies, method_registry


@pytest.fixture
def method_options():
    return {
        'name': 'testpaymentmethod',
        'fee_per_transaction': Decimal('0.30'),
        'fee_percent': Decimal('2.9'),
        'display_name': 'test_display_name',
        'currencies': ['EUR']
    }

class TestPaymentMethod:
    """
    Base class for all the payment method.
    """
    def test_payment_method_fees(self):
        b = BasePaymentMethod({
            'name': 'testpaymentmethod',
            'fee_per_transaction': Decimal('0.30'),
            'fee_percent': Decimal('2.9'),
            'display_name': 'test_display_name',
            'currencies': ['EUR']
        })
        assert b.calculate_fee(Decimal('100')) == Decimal('3.2')

    def test_payment_method_without_name(self):
        """
        Creating a payment class without a 'name' member variable should raise
        an exception.
        """
        with pytest.raises(PaymentMethodDoesNotHaveName):
            b = BasePaymentMethod({
                'display_name': 'test_display_name',
                'currencies': ['EUR']
            })

    def test_payment_method_without_currencies(self):
        """
        Creating a payment class without a 'currencies' member variable should raise
        an exception.
        """
        with pytest.raises(PaymentMethodDoesNotHaveCurrencies):
            b = BasePaymentMethod({
                'name': 'test_name',
                'display_name': 'test_display_name'
            })

    def test_concrete_payment_method_creation(self):
        """
        Create a concrete example of a payment method.
        """
        class SuperPay(BasePaymentMethod):
            pass
        options = {
            'name': 'superpay',
            'display_name': 'test_display_name',
            'currencies': ['EUR']
        }
        instance = SuperPay(options)
        assert isinstance(instance, SuperPay)
        assert method_registry['superpay'] == instance

    def test_verify(self, method_options):
        b = BasePaymentMethod({
            'name': 'testpaymentmethod',
            'fee_per_transaction': Decimal('0.30'),
            'fee_percent': Decimal('2.9'),
            'display_name': 'test_display_name',
            'currencies': ['EUR']
        })
        assert b.calculate_fee(Decimal('100')) == Decimal('3.2')
