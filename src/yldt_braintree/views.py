#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import braintree
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from campaigns.models import Transaction
from forms import BrainTreeForm
from yldt_braintree.models import BrainTreeTransaction


braintree_config = settings.YLDT_PAYMENT['braintree']

braintree.Configuration.configure(braintree.Environment.Sandbox,
        merchant_id=braintree_config['merchant_id'],
        public_key=braintree_config['public_key'],
        private_key=braintree_config['private_key'])

def do_transaction(transaction, form):
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

def payment_form(request, transaction_pk):
    """
    Show a payment form to the user.
    """
    transact = get_object_or_404(Transaction, pk=transaction_pk)
    if transact.state != Transaction.STATE_PLEDGED:
        return render(request, 'yldt_braintree/transaction_error.html',
                {'transaction': transact})

    client_side_encryption_key = braintree_config['cse_key']

    # process the payment data and show the results.
    if request.method == "POST":
        form = BrainTreeForm(request.POST)
        if form.is_valid():
            result = do_transaction(transact, form)

            if result.is_success:
                BrainTreeTransaction.objects.create(transaction=transact,
                        braintree_transaction_id=result.transaction.id)
                transact.state = Transaction.STATE_PAYMENT_CONFIRMED
                transact.save()
                url = reverse('yldt_braintree_payment_success', args=(transact.id, ))
                return HttpResponseRedirect(url)
            else:
                context = {
                    'braintree_error': result.message,
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
            'client_side_encryption_key': client_side_encryption_key,
            'form': BrainTreeForm()
        }
        return render(request, 'yldt_braintree/payment_form.html', context)

def payment_succes(request, transaction_pk):
    transact = get_object_or_404(Transaction, pk=transaction_pk)
    return render(request, 'yldt_braintree/payment_success.html',
            {'transaction': transact})