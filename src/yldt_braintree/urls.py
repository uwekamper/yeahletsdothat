#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# import views

urlpatterns = patterns('',
    url(r'^(?P<transaction_pk>\d+)/$', 'yldt_braintree.views.payment_form', name='yldt_braintree_payment_form'),
    url(r'^success/$', 'yldt_braintree.views.payment_succes', name='yldt_braintree_payment_success'),
    # url(r'^(?P<key>\w+)/$', 'campaigns.views.campaign_details', name='campaign_details'),
    # url(r'^(?P<key>\w+)/pay/$', 'campaigns.views.select_payment', name='select_payment'),
)