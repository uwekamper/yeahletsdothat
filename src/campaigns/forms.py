#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from campaigns.utils import get_payment_methods, get_payment_method_names

import models

class SelectPaymentForm(forms.Form):
    def __init__(self, campaign, *args, **kwargs):
        super(SelectPaymentForm, self).__init__(*args, **kwargs)
        self._campaign = campaign

    payment_method = forms.ChoiceField(choices=get_payment_method_names())
    amount = forms.DecimalField()

    def clean(self):
        cleaned_data = super(SelectPaymentForm, self).clean()
        min_amount = self._campaign.pledge_value
        if cleaned_data.get('amount') < min_amount:
            raise forms.ValidationError('Amount must be at least {}.'.format(min_amount))
        return cleaned_data

class ActivityForm(forms.ModelForm):
    v = forms.CharField(required=False)

    class Meta:
        model = models.Campaign
        fields = ('v',)


class NewActivityForm(forms.ModelForm):
    currency = forms.ChoiceField(choices=models.Campaign.CURRENCIES,
        widget=forms.Select(attrs={'class': 'form-control'}))

    target_account = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super(NewActivityForm, self).__init__(*args, **kwargs)
        self.fields['target_account'].queryset = models.BankAccount.objects.filter(user=user)

    class Meta:
        fields = ('name', 'description', 'goal', 'pledge_value', 'currency',
            'target_account',
            'min_people', 'max_people',
            'start_date', 'end_date', 'is_private')
        model = models.Campaign


class TransactionForm(forms.ModelForm):
    class Meta:
        fields = ('amount', 'return_btc_address', 'email')
        model = models.Transaction


class BankAccountForm(forms.ModelForm):
    class Meta:
        fields = ('description', 'btc_address')
        model = models.BankAccount