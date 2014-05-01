#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# import views

urlpatterns = patterns('',
    url(r'^(?P<transaction_pk>\d+)/$', 'yldt_braintree.views.payment_form'),
    url(r'^(?P<transaction_pk>\d+)/success/$', 'yldt_braintree.views.payment_succes'),
)