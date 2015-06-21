#!/usr/bin/python
# -*- coding: utf-8 -*-

from decimal import Decimal
from mock import MagicMock, Mock
from django.test import TestCase, Client
import braintree
from django.conf import settings
from campaigns.payment_method import get_method_by_name

from views import store_customer_id

class BrainTreeTest(TestCase):

    def setUp(self):
        self.payment_method = get_method_by_name('braintree')
        self.transaction = Mock()
        self.transaction.amount = Decimal('23.42')

    def test_store_customer_id(self):
        store_customer_id(self.payment_method, self.transaction)

