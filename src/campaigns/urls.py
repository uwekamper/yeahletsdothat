#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'uk'

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',

    url(r'^new/$', 'campaigns.views.new_activity', name='new_activity'),
    url(r'^(?P<key>\w+)/$', 'campaigns.views.campaign_details', name='campaign_details'),
    url(r'^(?P<key>\w+)/pay/$', 'campaigns.views.select_payment', name='select_payment'),

)