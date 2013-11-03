#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Activity(models.Model):
    CURRENCY_EUR = (0, _('EUR'))
    CURRENCY_USD = (1, _('USD'))

    CURRENCIES = (
        CURRENCY_EUR,
        CURRENCY_USD,
    )

    name = models.CharField(max_length=200)
    currency = models.IntegerField(choices=CURRENCIES)
    goal = models.DecimalField(max_digits=6, decimal_places=2)
    pledge_value = models.DecimalField(max_digits=6, decimal_places=2)
    min_people = models.IntegerField()
    max_people = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()