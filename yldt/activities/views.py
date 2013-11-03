#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import forms

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
