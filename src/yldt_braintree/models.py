#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from campaigns.models import Transaction

class BrainTreeTransaction(models.Model):
    transaction = models.ForeignKey(Transaction)
    braintree_transaction_id = models.CharField(max_length=255)