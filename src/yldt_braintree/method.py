#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from campaigns.payment_method import BasePaymentMethod

class BrainTree(BasePaymentMethod):

    def __init__(self, options):
        # super-class gets the name, display_name and currencies
        super(BrainTree, self).__init__(options)

        # copy the options that are specific to this module
        self.merchant_id = options['merchant_id']
        self.public_key = options['public_key']
        self.private_key = options['private_key']
        self.cse_key = options['cse_key']

    def pay(self, campaign, transaction):
        url = '/pay/' + self.name + '/' + str(transaction.id) + '/'
        return HttpResponseRedirect(url)

    def refund(self, campaign, transaction):
        pass