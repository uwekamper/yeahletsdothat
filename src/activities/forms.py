#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

import models


class NewActivityForm(forms.ModelForm):
    currency = forms.ChoiceField(choices=models.Activity.CURRENCIES,
        widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        fields = ('name', 'description', 'goal', 'pledge_value', 'currency',
            'min_people', 'max_people',
            'start_date', 'end_date')
        model = models.Activity


class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction


class BankAccountForm(forms.ModelForm):
    class Meta:
        fields = ('description', 'btc_address')
        model = models.BankAccount