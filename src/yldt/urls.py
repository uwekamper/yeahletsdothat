#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

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
    url(r'^transaction/(?P<pk>\d+)/$', 'campaigns.views.transaction', name='transaction'),
    # url(r'^api/transaction/(?P<pk>\d+)/$', 'campaigns.views.transaction_api', name='transaction_api'),

    url(r'^yeah/', include('campaigns.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

for options in settings.YLDT_PAYMENT_METHODS:
    module = __import__(options['module_name'])
    method = module.PaymentMethod(options)
    print('Found payment method %s' % options['module_name'])
    # create a url pattern for the plugin.
    pattern = r'^pay/' + method.name.encode('string-escape') + r'/'
    include_module = options['module_name'] + '.urls'
    sub_url = url(pattern, include(include_module), {'payment_method_name': method.name})
    urlpatterns.append(sub_url)

print urlpatterns