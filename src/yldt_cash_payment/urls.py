#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# import views

urlpatterns = patterns('',
    url(r'^(?P<transaction_id>[\w-]+)/$', 'yldt_cash_payment.views.payment_info',
        name='cash_payment_info'),
    url(r'^(?P<transaction_id>[\w-]+)/edit/$', 'yldt_cash_payment.views.payment_edit',
        name='cash_payment_edit'),
)