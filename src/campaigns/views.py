#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect, \
    HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
import jsonrpclib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from campaigns.payment_method import get_method_by_name
from campaigns.serializers import TransactionSerializer
from campaigns.utils import get_campaign_or_404, get_payment_methods

import forms
from models import Campaign, Transaction, BankAccount
from django.conf import settings


def index(request):
    return render(request, 'campaigns/index.html', {})

@login_required
def user_profile(request):
    campaigns = Campaign.objects.filter(user=request.user)
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'campaigns/user_profile.html',
        {'accounts': accounts, 'campaigns': campaigns})

def current_activities(request):
    pass

@login_required
def manage_bankaccounts(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'campaigns/manage_bankaccounts.html', {'accounts': accounts})

@login_required
def add_bankaccount(request):
    """
    TODO: Write docstring
    """
    if request.method == 'POST':
        form = forms.BankAccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return HttpResponseRedirect(reverse('manage_bankaccounts'))
        else:
            return render(request, 'campaigns/add_bankaccount.html', {'form': form})

    form = forms.BankAccountForm()
    return render(request, 'campaigns/add_bankaccount.html', {'form': form})

@login_required
def new_activity(request):
    """
    View for creating new activities.
    """
    # if request.method == 'POST':
    #     form = forms.NewCampaignForm(request.user, request.POST)
    #     if form.is_valid():
    #         new_campaign = form.save(commit=False)
    #         new_campaign.user = request.user
    #         new_campaign.save()
    #         url = reverse('campaign_details', args=(new_campaign.key,))
    #         return HttpResponseRedirect(url)
    #     else:
    #         print form.errors
    #         return render(request, 'campaigns/new_campaign.html', {'form': form})

    form = forms.NewCampaignForm(user=request.user)
    return render(request, 'campaigns/new_campaign.html', {'form': form})


def campaign_details(request, key):
    """
    View that shows a single activity.
    """
    campaign = get_campaign_or_404(request, key)
    methods = get_payment_methods()
    context = {'campaign': campaign, 'methods': methods, }

    try:
        if settings.YLDT_PLEDGE_BUTTON_TEXT:
            context['pledge_button_text'] = settings.YLDT_PLEDGE_BUTTON_TEXT
    except AttributeError:
        pass

    return render(request, 'campaigns/campaign_details.html', context)

def abort_activity(request, pk):
    """
    Abort an already started activity. If there are any already confirmed payments,
    they will be refunded.
    """
    # TODO: Implement abort feature
    return None

def get_rpc_address(conf=None):
    if not conf:
        conf = settings
    return 'http://{}:{}@{}:{}/'.format(conf.BTC_USER, conf.BTC_PASS, conf.BTC_HOST, conf.BTC_PORT)

def create_bitcoin_address(address=None):
    if not address:
        address = get_rpc_address()
    server = jsonrpclib.Server(address)
    new_addr = server.getnewaddress()
    return new_addr

def select_payment(request, key):
    """
    The user has clicked the "Pledge now" button. Let's show him the list of
    available Payment methods
    """
    campaign = get_campaign_or_404(request, key)

    # TODO: is this necessary?
    methods = get_payment_methods()

    if request.method == 'POST':
        form = forms.SelectPaymentForm(campaign, request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            method = get_method_by_name(form.cleaned_data.get('payment_method'))

            # Create a new payment transaction, STATE_PLEDGE means that the user wants
            # to pay but has not payed, yet.
            transact = Transaction.objects.create(amount=amount, campaign=campaign,
                    state=Transaction.STATE_PLEDGED)

            # Delegate the payment transaction to the pay() method of the selected
            # payment method. The method will then redirect the user to the page it needs
            # to complete the payment.
            return method.pay(campaign, transact)

        else:
            return render(request, 'campaigns/select_payment.html',
                    {'campaign': campaign, 'methods': methods, 'form': form})

    else:
        return render(request, 'campaigns/select_payment.html',
                {'campaign': campaign, 'methods': methods})

def transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'campaigns/transaction.html',
            {'transaction': transaction, 'activity': transaction.campaign})

def check_completion(activity):
    amount = activity.get_total_pledge_amount()

    if amount >= activity.goal and not activity.completed:
        # set the activity to completed so no one else can pledge.
        activity.completed = True
        activity.save()

        s = jsonrpclib.Server(get_rpc_address())
        s.sendtoaddress(activity.target_account.btc_address, float(activity.goal),
            'buy-uk-a-beer')


@api_view(['GET'])
def transaction_api(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    s = jsonrpclib.Server(get_rpc_address())
    received = s.getreceivedbyaddress(transaction.btc_address, 0)
    confirmed = s.getreceivedbyaddress(transaction.btc_address, 1)

    print "received: ", received
    print "confirmed: ", confirmed

    # TODO: this should be moved into a background task
    if transaction.state == Transaction.STATE_PLEDGED:
        if received >= float(transaction.amount):
            transaction.state = Transaction.STATE_PAYMENT_RECEIVED
            transaction.save()
        if confirmed >= float(transaction.amount):
            transaction.state = Transaction.STATE_PAYMENT_CONFIRMED
            transaction.save()
    elif transaction.state == Transaction.STATE_PAYMENT_RECEIVED:
        if confirmed >= float(transaction.amount):
            transaction.state = Transaction.STATE_PAYMENT_CONFIRMED
            transaction.save()

    check_completion(transaction.campaign)

    # transaction.state = 0
    ser = TransactionSerializer(transaction)
    return Response(ser.data)

