#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import forms
from models import Activity, Transaction, BankAccount


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
        form = forms.NewActivityForm(request.POST)
        if form.is_valid():

            new_activity = form.save(commit=False)
            new_activity.user = request.user
            new_activity.save()
            return HttpResponseRedirect(reverse('activity', args=(new_activity.id,)))
        else:
            print form.errors
            return render(request, 'activities/new_activity.html', {'form': form})

    form = forms.NewActivityForm()
    return render(request, 'activities/new_activity.html', {'form': form})

def activity(request, pk):
    """
    View that shows a single activity.
    """
    activity = get_object_or_404(Activity, pk=pk)
    context = {'activity': activity, }
    return render(request, 'activities/activity.html', context)

def pledge_activity(request, pk):
    """
    This view lets users pledge on activities.
    """
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = forms.TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            context = {'activity': activity, 'transaction': transaction}
            return render(request, 'activities/pledged.html', context)
        else:
            return HttpResponseNotAllowed('Wrong!')
    else:
        raise HttpResponseNotAllowed('POST only.')
