#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^(?P<transaction_id>[\w-]+)/$', views.payment_form),
    url(r'^(?P<transaction_id>[\w-]+)/success/$', views.payment_succes),
]