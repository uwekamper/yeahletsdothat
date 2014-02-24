from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yldt.views.home', name='home'),
    # url(r'^yldt/', include('yldt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$', 'activities.views.user_profile', name="user_profile"),

    url(r'^bankaccounts/$', 'activities.views.manage_bankaccounts', name='manage_bankaccounts'),
    url(r'^bankaccounts/add/$', 'activities.views.add_bankaccount', name='add_bankaccount'),

    url(r'^transaction/(?P<pk>\d+)/$', 'activities.views.transaction', name='transaction'),
    url(r'^api/transaction/(?P<pk>\d+)/$', 'activities.views.transaction_api', name='transaction_api'),
    url(r'^activities/new/$', 'activities.views.new_activity', name='new_activity'),
    url(r'^activities/(?P<pk>\d+)/$', 'activities.views.activity', name='activity'),
    url(r'^activities/(?P<pk>\d+)/pledge/$', 'activities.views.pledge_activity',
        name='pledge_activity'),
)
