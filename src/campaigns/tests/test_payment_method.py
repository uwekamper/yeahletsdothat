import pytest
from campaigns.payment_method import BasePaymentMethod, PaymentMethodDoesNotHaveName, \
    PaymentMethodDoesNotHaveCurrencies, method_registry

class TestPaymentMethod:

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

