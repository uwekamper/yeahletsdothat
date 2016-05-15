# -*- coding: utf-8 -*-
from django.shortcuts import render
from campaigns import commands
from campaigns.models import Campaign, Transaction
from yldt_cash_payment.forms import CashPaymentForm


def payment_info(request, transaction_id, payment_method_name):
    """
    Show information to the user.
    """
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    campaign = transaction.campaign
    user = campaign.user
    context = {
        'transaction': transaction,
        'campaign': campaign,
        'initiator': user
    }
    return render(request, 'yldt_cash_payment/cash_payment_info.html', context)

def payment_edit(request, transaction_id, payment_method_name):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    if request.method == 'POST':
        form = CashPaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            commands.ReceivePaymentCommand(transaction_id, amount, request)
            context = {
                'transaction': transaction,
                'campaign': transaction.campaign,
                'amount': amount
            }
            return render(request, 'yldt_cash_payment/cash_payment_successful.html', context)
        else:
            context = {
                'transaction': transaction,
                'campaign': transaction.campaign,
                'form': form
            }
        return render(request, 'yldt_cash_paycment/cash_payment_edit.html', context)

    # GET request
    form = CashPaymentForm()
    context = {
        'transaction': transaction,
        'campaign': transaction.campaign,
        'form': form
    }
    return render(request, 'yldt_cash_payment/cash_payment_edit.html', context)
