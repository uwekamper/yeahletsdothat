#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'uk'

from django.conf.urls import patterns, include, url
from .models import Campaign, Perk
from rest_framework import viewsets, routers
from campaigns.serializers import CampaignSerializer, PerkSerializer
from rest_framework.response import Response


class CampaignsViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field = 'key'


class PerksViewSet(viewsets.ModelViewSet):
    model = Perk
    queryset = Perk.objects.all()
    serializer_class = PerkSerializer

    def list(self, request):
        queryset = Perk.objects.all()
        campaign_key = request.GET.get('campaign', None)
        if campaign_key is not None:
            queryset = Perk.objects.filter(campaign__key=campaign_key)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'campaigns', CampaignsViewSet)
router.register(r'perks', PerksViewSet)

urlpatterns = patterns('',
    url(r'^$', 'campaigns.views.campaign_index', name='campaign_index'),
    url(r'^rest/', include(router.urls)),
    url(r'^(?P<key>[\w=-]+)/pay/$', 'campaigns.views.select_payment', name='select_payment'),
    url(r'^new/$', 'campaigns.views.campaign_new', name='campaign_new'),
    url(r'^(?P<key>[\w=-]+)/$', 'campaigns.views.campaign_details', name='campaign_details'),
    url(r'^(?P<key>[\w=-]+)/transactions/$', 'campaigns.views.campaign_show_transactions',
        name='campaign_show_transactions'),
    url(r'^(?P<key>[\w=-]+)/edit/$', 'campaigns.views.campaign_edit', name='campaign_edit'),
)