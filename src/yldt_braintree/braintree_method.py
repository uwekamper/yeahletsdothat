#!/usr/bin/python
# -*- coding: utf-8 -*-

import braintree
from django.http import HttpResponseRedirect

from campaigns.payment_method import BasePaymentMethod
from campaigns.payment_method import PaymentException
from campaigns.models import Transaction


class BrainTreeException(PaymentException):
    pass

class BrainTreeTransactionNotVerifiedException(BrainTreeException):
    pass

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

        braintree.Configuration.configure(
            self.braintree_environment,
            merchant_id=self.merchant_id,
            public_key=self.public_key,
            private_key=self.private_key
        )

    def pay(self, request, campaign, transaction_id):
        url = '/pay/' + self.name + '/' + str(transaction_id) + '/'
        return HttpResponseRedirect(url)

    #TODO: We prob. do not need a verify() in this interface
    def verify(self, request, transaction_id):
        """
        Verify that the supplied credit card (represented by the payment method
        nonce) can indeed be used to deduct money at the current time.
        Will issue a VerifyPaymentAction.
        """
        braintree_trans = BrainTreeTransaction.objects.get(transaction_id=transaction_id)
        t = Transaction.objects.get(transaction_id=transaction_id)

    def charge(self, transaction_id):
        """
        We get the Braintree customer object and try to charge the customer's credit card.
        """
        braintree.Configuration.configure(self.braintree_environment,
            merchant_id=self.merchant_id,
            public_key=self.public_key,
            private_key=self.private_key)

        transaction = Transaction.objects.get(transaction_id=transaction_id)
        if transaction.state != Transaction.STATE_VERIFIED:
            raise BrainTreeTransactionNotVerifiedException('Transaction {} is '
                    'not in the verified state.'.format(transaction_id))

    def refund(self, campaign, transaction):
        pass

    def is_sandbox(self):
        return self.braintree_environment == braintree.Environment.Sandbox

    def get_client_token(self):
        return braintree.ClientToken.generate()

    def validate_nonce(self, amount, payment_nonce):
        result = braintree.Transaction.sale({
            "amount": amount,
            "payment_method_nonce": payment_nonce,
        })
        if result.is_success:
            return True
        return False

    def get_json(self):
        result = {
            'client_token': self.get_client_token(),
        }
        return result


