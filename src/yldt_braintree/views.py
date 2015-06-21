#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import braintree
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from campaigns.commands import ReceivePayment

from campaigns.models import Transaction
from campaigns.payment_method import get_method_by_name
from forms import BrainTreeForm
from yldt_braintree.models import BrainTreeTransaction

def store_
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
        'credit_card': {
            'number': form.cleaned_data['number'],
            'cvv': form.cleaned_data['cvv'],
            'expiration_month': form.cleaned_data['month'],
            'expiration_year': form.cleaned_data['year']
        },
        'options': {
            'submit_for_settlement': True
        }
    })

    return result

def payment_form(request, transaction_id, payment_method_name):
    """
    Show a payment form to the user.
    """
    transact = get_object_or_404(Transaction, transaction_id=transaction_id)
    if transact.state != Transaction.STATE_OPEN:
        return render(request, 'yldt_braintree/transaction_error.html',
                {'transaction': transact})

    payment_method = get_method_by_name(payment_method_name)
    client_side_encryption_key = payment_method.cse_key

    amount = transact.amount
    fee = payment_method.calculate_fee(amount)
    total = amount + fee

    # process the payment data and show the results.
    if request.method == "POST":
        form = BrainTreeForm(request.POST)
        if form.is_valid():
            result = do_transaction(payment_method, transact, form)

            if result.is_success:
                # TODO: store the customer ID in the database
                # BrainTreeTransaction.objects.create(transaction_id=transaction_id,
                #    braintree_transaction_id=result.transaction.id)

                ReceivePayment(transaction_id, transact.amount, request)

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
                    'client_side_encryption_key': client_side_encryption_key,
                    'form': form
                }
                return render(request, 'yldt_braintree/payment_form.html', context)

        # The user entered invalid data
        else:
            context = {
                'transaction': transact,
                'client_side_encryption_key': client_side_encryption_key,
                'form': form
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
            'client_side_encryption_key': client_side_encryption_key,
            'form': BrainTreeForm()

        }
        return render(request, 'yldt_braintree/payment_form.html', context)

def payment_succes(request, transaction_id, payment_method_name):
    transact = get_object_or_404(Transaction, transaction_id=transaction_id)
    return render(request, 'yldt_braintree/payment_success.html',
            {'transaction': transact})