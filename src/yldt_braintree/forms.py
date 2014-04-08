#!/usr/bin/python2
# -*- coding: utf-8 -*-

# from django.db import models
from django import forms


class BrainTreeForm(forms.Form):
    """
    The form used for credit card data
    """
    # All the values are encrypted by the javascript before we get them.
    # That is the reason, why all these fields are so large.
    number = forms.CharField(max_length=1024)
    cvv = forms.CharField(max_length=1024)
    month = forms.CharField(max_length=1024)
    year = forms.CharField(max_length=1024)