#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^(?P<transaction_id>[\w-]+)/$', views.payment_info, name='cash_payment_info'),
    url(r'^(?P<transaction_id>[\w-]+)/edit/$', views.payment_edit, name='cash_payment_edit'),
]