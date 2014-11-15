#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from campaigns.models import Transaction, Campaign, Perk

class CampaignSerializer(serializers.ModelSerializer):
    """
    # TODO: Write docs
    """
    target_account = serializers.PrimaryKeyRelatedField(default=1, required=False)
    class Meta:
        model = Campaign

class PerkSerializer(serializers.ModelSerializer):
    """
    TODO: write docs
    """
    state = serializers.SerializerMethodField('get_state')

    def get_state(self, obj):
        """
        Add an constant state: "OK" field in the output for the UI
        """
        return 'OK'

    class Meta:
        model = Perk
        fields = ('id', 'campaign', 'title', 'text', 'amount', 'available', 'state')

class TransactionSerializer(serializers.ModelSerializer):
    """
    TODO: Write docs
    """
    pledged = serializers.SerializerMethodField('_get_pledged')
    received = serializers.SerializerMethodField('_get_received')
    confirmed = serializers.SerializerMethodField('_get_confirmed')

    def _get_pledged(self, obj):
        return(obj.state == Transaction.STATE_PLEDGED)

    def _get_received(self, obj):
        return(obj.state == Transaction.STATE_PAYMENT_RECEIVED)

    def _get_confirmed(self, obj):
        return(obj.state == Transaction.STATE_PAYMENT_CONFIRMED)

    class Meta:
        model = Transaction
        fields = ('id', 'activity', 'state', 'pledged', 'received', 'confirmed')