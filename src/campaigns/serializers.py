#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from campaigns.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    TODO
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