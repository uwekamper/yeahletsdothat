#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import gettext_lazy as _
from campaigns.utils import get_payment_methods, get_payment_method_names

import models

class SelectPaymentForm(forms.Form):
    def __init__(self, campaign, *args, **kwargs):
        super(SelectPaymentForm, self).__init__(*args, **kwargs)
        self._campaign = campaign

    payment_method = forms.ChoiceField(choices=get_payment_method_names())
    amount = forms.DecimalField()
    email1 = forms.EmailField()
    email2 = forms.EmailField()

    def clean(self):
        cleaned_data = super(SelectPaymentForm, self).clean()
        min_amount = self._campaign.pledge_value

        # the amount may not be
        if cleaned_data.get('amount') < min_amount:
            raise forms.ValidationError('Amount must be at least {}.'.format(min_amount))

        # make sure the e-mail addresses are correct
        if cleaned_data.get('email1') != cleaned_data.get('email2'):
            raise forms.ValidationError(_('Both e-mail addresses must be equal.'))
        return cleaned_data

class ActivityForm(forms.ModelForm):
    v = forms.CharField(required=False)

    class Meta:
        model = models.Campaign
        fields = ('v',)


class NewCampaignForm(forms.ModelForm):
    currency = forms.ChoiceField(choices=models.Campaign.CURRENCIES,
        widget=forms.Select(attrs={'class': 'form-control'}))

    target_account = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super(NewCampaignForm, self).__init__(*args, **kwargs)
        self.fields['target_account'].queryset = models.BankAccount.objects.filter(user=user)

    class Meta:
        fields = ('name', 'description', 'goal', 'currency',
            'target_account',
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