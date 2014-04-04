#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# import views

urlpatterns = patterns('',
    url(r'test/$', 'yldt_braintree.views.bla', name='yldt_braintree_bla'),
    # url(r'^(?P<key>\w+)/$', 'campaigns.views.campaign_details', name='campaign_details'),
    # url(r'^(?P<key>\w+)/pay/$', 'campaigns.views.select_payment', name='select_payment'),
)