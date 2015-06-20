#!/usr/bin/python
# -*- coding: utf-8 -*-

import braintree
from django.http import HttpResponseRedirect

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
        braintree_env = options.get('environment', 'sandbox')
        if braintree_env == 'production':
            self.braintree_environment = braintree.Environment.Production
        else:
            self.braintree_environment = braintree.Environment.Sandbox


    def pay(self, campaign, transaction_id):
        url = '/pay/' + self.name + '/' + str(transaction_id) + '/'
        return HttpResponseRedirect(url)

    def refund(self, campaign, transaction):
        pass

    def is_sandbox(self):
        return self.braintree_environment == braintree.Environment.Sandbox

    def get_client_token(self):
        braintree.Configuration.configure(
            self.braintree_environment,
            merchant_id=self.merchant_id,
            public_key=self.public_key,
            private_key=self.private_key
        )
        return braintree.ClientToken.generate()