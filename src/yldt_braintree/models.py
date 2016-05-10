#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class BrainTreeTransaction(models.Model):
    transaction_id = models.CharField(max_length=255)
    payment_method_nonce = models.CharField(max_length=1024, null=True, blank=True)
    payment_method_nonce = models.CharField(max_length=1024, null=True, blank=True)
    braintree_customer_id = models.CharField(max_length=2048, null=True, blank=True)
    braintree_transaction_id = models.CharField(max_length=255, null=True, blank=True)

