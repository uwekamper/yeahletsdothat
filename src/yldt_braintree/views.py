#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import braintree
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from campaigns.commands import ReceivePaymentCommand, VerifyPaymentCommand

from campaigns.models import Transaction
from campaigns.payment_method import get_method_by_name
from . forms import BrainTreeForm
from . models import BrainTreeTransaction

def store_customer_id(method, transaction):
    return False

def do_transaction(payment_method, transaction, form):
    """
    Subroutine that send the transaction data to the Braintree servers.
    """
    # configure the environment
    braintree.Configuration.configure(payment_method.braintree_environment,
            merchant_id=payment_method.merchant_id,
            public_key=payment_method.public_key,
            private_key=payment_method.private_key)

    # create the transaction on Braintree's side
    result = braintree.Transaction.sale({
        'amount': "{0:.2f}".format(transaction.amount),
    })

    return result

def create_customer(request, transaction, payment_method_nonce):
    """
    Try to create a customer in the braintree database.
    """
    first_name, last_name = transaction.name.rsplit(' ', 1)
    result = braintree.Customer.create({
        "first_name": first_name,
        "last_name": last_name,
        "email": transaction.email,
        "credit_card": {
            "payment_method_nonce": payment_method_nonce,
            "options": {
                "verify_card": True
            }
        }
    })
    return result

def store_verification_result(transaction_id, result):
    """
    Store the data from a successful credit card verification in the database
    so that we can use the customer ID to get the money once the campaign is finished.
    """
    bt, created = BrainTreeTransaction.objects.get_or_create(transaction_id=transaction_id)
    bt.braintree_customer_id = result.customer.id
    print(result)
    #bt.payment_method_token = result.payment_method_token
    bt.save()
    VerifyPaymentCommand(transaction_id)

def payment_form(request, transaction_id, payment_method_name):
    """
    Show a payment form to the user.
    """
    transact = get_object_or_404(Transaction, transaction_id=transaction_id)
    if transact.state != Transaction.STATE_UNVERIFIED:
        return render(request, 'yldt_braintree/transaction_error.html',
                {'transaction': transact})
    payment_method = get_method_by_name(payment_method_name)

    first_name, last_name = transact.name.split(' ', 2)
    amount = transact.amount
    fee = payment_method.calculate_fee(amount)
    total = amount + fee

    # process the payment data and show the results.
    if request.method == "POST":
        form = BrainTreeForm(request.POST)
        if form.is_valid():
            result = create_customer(request, transaction, nonce_from_the_client)
            if result.is_success:
                store_verification_result(result)
                url = '/pay/{}/{}/success/'.format(payment_method_name, transaction_id)
                return HttpResponseRedirect(url)
            else:
                context = {
                    'braintree_error': result.message,
                    'amount': amount,
                    'fee': fee,
                    'total': total,
                    'is_sandbox': payment_method.is_sandbox(),
                    'transaction': transact,
                    'client_token': payment_method.get_client_token(),
                    'form': form,
                }
                return render(request, 'yldt_braintree/payment_form.html', context)

        # The user entered invalid data
        else:
            print('{}'.format(form.errors))
            context = {
                'transaction': transact,
                'amount': amount,
                'fee': fee,
                'total': total,
                'is_sandbox': payment_method.is_sandbox(),
                'client_token': payment_method.get_client_token(),
                'form': form,

            }
            return render(request, 'yldt_braintree/payment_form.html', context)

    # show the payment form to the user.
    else:
        context = {
            'transaction': transact,
            'amount': amount,
            'fee': fee,
            'total': total,
            'is_sandbox': payment_method.is_sandbox(),
            'client_token': payment_method.get_client_token(),
            'form': BrainTreeForm(),
        }
        return render(request, 'yldt_braintree/payment_form.html', context)

def payment_succes(request, transaction_id, payment_method_name):
    transact = get_object_or_404(Transaction, transaction_id=transaction_id)
    return render(request, 'yldt_braintree/payment_success.html',
            {'transaction': transact})