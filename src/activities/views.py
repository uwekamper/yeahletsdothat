#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404

import forms

from models import Activity, Transaction

@login_required
def user_profile(request):
    return render(request, 'activities/user_profile.html', {})

def current_activities(request):
    pass

@login_required
def new_activity(request):
    """
    View for creating new activities.
    """
    if request.method == 'POST':
        form = forms.NewActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'activities/new_activity_successful.html', {})
        else:
            return render(request, 'activities/new_activity_successful.html',
                {'form': form})

    form = forms.NewActivityForm()
    return render(request, 'activities/new_activity_wizard.html', {'form': form})

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
