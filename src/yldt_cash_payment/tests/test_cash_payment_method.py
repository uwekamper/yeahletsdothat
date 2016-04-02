# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import pytest

from decimal import Decimal
import yldt_cash_payment.views
from yldt_cash_payment.cash_payment_method import PaymentMethod
from campaigns.tests.common import campaign, transaction_id, client

@pytest.fixture
def config():
    return {
        'module_name': 'yldt_cash_payment',
        'name': 'cash',
        'display_name': 'Cash in de Täsch',
        'currencies': ['EUR'],
        # 'fee_per_transaction': Decimal('0.0'),
        # 'fee_percent': Decimal('0.0'),
    }

@pytest.fixture
def payment_inst(config):
    return PaymentMethod(config)


class TestPaymentMethod:
    """
    Test the payment method class for cash payments
    """
    def test_payment_method_creation(self, config):
        b = PaymentMethod(config)
        assert b.name == config['name']
        assert b.display_name == config['display_name']
        assert b.currencies == config['currencies']

    def test_get_actions(self):
        pass

    def test_payment_method_fees(self, payment_inst):
        assert payment_inst.calculate_fee(Decimal('100')) == Decimal('0.0')

    @pytest.mark.django_db
    def test_pay(self, payment_inst, campaign, transaction_id):
        response = payment_inst.pay(None, campaign.key, transaction_id)
        url = reverse(yldt_cash_payment.views.payment_info, args=[transaction_id])
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == url

    @pytest.mark.django_db
    def test_payment_info(self, campaign, transaction_id, client):
        url = reverse(yldt_cash_payment.views.payment_info, args=[transaction_id])
        response = client.get(url)

    def test_complete(self, payment_inst):
        pass

    def test_refund(self):
        pass
