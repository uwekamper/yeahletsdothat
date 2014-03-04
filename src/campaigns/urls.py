#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'uk'

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',

    url(r'^new/$', 'campaigns.views.new_activity', name='new_activity'),
    url(r'^(?P<key>\w+)/$', 'campaigns.views.activity', name='activity'),
    url(r'^(?P<key>\w+)/pledge/$', 'campaigns.views.pledge_activity', name='pledge_activity'),

)