#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

# import campaigns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yldt.views.home', name='home'),
    # url(r'^yldt/', include('yldt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'campaigns.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$', 'campaigns.views.user_profile', name="user_profile"),

    url(r'^bankaccounts/$', 'campaigns.views.manage_bankaccounts', name='manage_bankaccounts'),
    url(r'^bankaccounts/add/$', 'campaigns.views.add_bankaccount', name='add_bankaccount'),

    url(r'^transaction/(?P<pk>\d+)/$', 'campaigns.views.transaction', name='transaction'),
    url(r'^api/transaction/(?P<pk>\d+)/$', 'campaigns.views.transaction_api', name='transaction_api'),

    url(r'^yeah/', include('campaigns.urls')),
)

for payment_plugin in settings.YLDT_PAYMENT_METHODS:
    method = __import__(payment_plugin)
    print('Found payment method %s' % payment_plugin)
    # create a url pattern for the plugin.
    pattern = r'^pay/' + method.PaymentMethod.name.encode('string-escape') + r'/'
    include_module = payment_plugin + '.urls'
    urlpatterns.append( url(pattern, include(include_module)) )

print urlpatterns