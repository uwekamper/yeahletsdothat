#!/usr/bin/python
# -*- coding: utf-8 -*-

from campaigns.payment_method import BasePaymentMethod


class BitCoin(BasePaymentMethod):

    def __init__(self, options):
        super(BitCoin, self).__init__(options)

    def pay(self, campaign, transaction):
        # TODO implement this
        pass

    def refund(self, campaign, transaction):
        pass