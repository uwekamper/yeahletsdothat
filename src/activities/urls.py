#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'uk'

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',

    url(r'^new/$', 'activities.views.new_activity', name='new_activity'),
    url(r'^(?P<pk>\d+)/$', 'activities.views.activity', name='activity'),
    url(r'^(?P<pk>\d+)/pledge/$', 'activities.views.pledge_activity', name='pledge_activity'),

)