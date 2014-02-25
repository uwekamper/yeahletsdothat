#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import jsonrpclib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from activities.serializers import TransactionSerializer

import forms
from models import Activity, Transaction, BankAccount
from django.conf import settings

@login_required
def user_profile(request):
    activities = Activity.objects.filter(user=request.user)
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'activities/user_profile.html',
        {'accounts': accounts, 'activities': activities})

def current_activities(request):
    pass

@login_required
def manage_bankaccounts(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'activities/manage_bankaccounts.html', {'accounts': accounts})

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
            return render(request, 'activities/add_bankaccount.html', {'form': form})

    form = forms.BankAccountForm()
    return render(request, 'activities/add_bankaccount.html', {'form': form})

@login_required
def new_activity(request):
    """
    View for creating new activities.
    """
    if request.method == 'POST':
        form = forms.NewActivityForm(request.POST, request.user)
        if form.is_valid():

            new_activity = form.save(commit=False)
            new_activity.user = request.user
            new_activity.save()
            return HttpResponseRedirect(reverse('activity', args=(new_activity.id,)))
        else:
            print form.errors
            return render(request, 'activities/new_activity.html', {'form': form})

    form = forms.NewActivityForm(user=request.user)
    return render(request, 'activities/new_activity.html', {'form': form})

def activity(request, pk):
    """
    View that shows a single activity.
    """
    activity = get_object_or_404(Activity, pk=pk)
    context = {'activity': activity, }
    return render(request, 'activities/activity.html', context)

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

def pledge_activity(request, pk):
    """
    This view lets users pledge on activities.
    """
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = forms.TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)

            # Create new bitcoin address for the transaction
            transaction.btc_address = create_bitcoin_address()
            transaction.activity = activity
            transaction.state = Transaction.STATE_PLEDGED
            transaction.save()
            return HttpResponseRedirect(reverse('transaction', args=(transaction.id,)))
        else:
            return render(request, 'activities/pledge_activity.html',
                    {'form': form, 'activity': activity})

    form = forms.TransactionForm(initial={'amount': activity.pledge_value})
    return render(request, 'activities/pledge_activity.html',
            {'form': form, 'activity': activity})


def transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'activities/transaction.html',
            {'transaction': transaction, 'activity': transaction.activity})

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

    check_completion(transaction.activity)

    # transaction.state = 0
    ser = TransactionSerializer(transaction)
    return Response(ser.data)

