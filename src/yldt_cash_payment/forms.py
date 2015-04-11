# -*- coding: utf-8 -*-

from django import forms

class CashPaymentForm(forms.Form):
    amount = forms.DecimalField(decimal_places=10, max_digits=20)