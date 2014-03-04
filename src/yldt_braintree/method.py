#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from campaigns.payment_method import BasePaymentMethod


class BrainTree(BasePaymentMethod):
    name = 'braintree'
    display_name = _('Braintree')
