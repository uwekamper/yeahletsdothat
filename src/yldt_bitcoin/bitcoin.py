#!/usr/bin/python
# -*- coding: utf-8 -*-

from campaigns.payment_method import BasePaymentMethod


class BitCoin(BasePaymentMethod):
    name = 'bitcoin'
    display_name = 'Bitcoin'