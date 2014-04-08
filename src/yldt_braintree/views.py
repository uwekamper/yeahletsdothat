#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import braintree
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from campaigns.models import Transaction
from forms import BrainTreeForm


braintree_config = settings.YLDT_PAYMENT['braintree']

braintree.Configuration.configure(braintree.Environment.Sandbox,
        merchant_id=braintree_config['merchant_id'],
        public_key=braintree_config['public_key'],
        private_key=braintree_config['private_key'])

def payment_form(request, transaction_pk):
    """
    TODO: Write docs
    """
    transact = get_object_or_404(Transaction, pk=transaction_pk)

    client_side_encryption_key = braintree_config['cse_key']

    if request.method == "POST":
        form = BrainTreeForm(request.POST)
        if form.is_valid():

            result = braintree.Transaction.sale({
                "amount": "1000.00",
                "credit_card": {
                    "number": form.cleaned_data["number"],
                    "cvv": form.cleaned_data["cvv"],
                    "expiration_month": form.cleaned_data["month"],
                    "expiration_year": form.cleaned_data["year"]
                },
                "options": {
                    "submit_for_settlement": True
                }
            })

            if result.is_success:
                return HttpResponse("<h1>Success! Transaction ID: {0}</h1>".format(result.transaction.id))
            else:
                return HttpResponse("<h1>Error: {0}</h1>".format(result.message))

        # The user entered invalid data
        else:
            context = {
                'client_side_encryption_key': client_side_encryption_key,
                'form': form
            }
            return render(request, 'yldt_braintree/payment_form.html', context)
    else:
        context = {
            'client_side_encryption_key': client_side_encryption_key,
            'form': BrainTreeForm()
        }
        return render(request, 'yldt_braintree/payment_form.html', context)