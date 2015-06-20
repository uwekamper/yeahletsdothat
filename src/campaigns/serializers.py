#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.encoding import smart_text

from rest_framework import serializers
from campaigns.models import Transaction, Campaign, Perk
from campaigns.utils import get_payment_methods


class PaymentPOSTData(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    name = serializers.CharField()
    payment_nonce = serializers.CharField()



class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk


class PaymentMethodSerializer(serializers.Serializer):
    """

    """
    module_name = serializers.CharField()
    name = serializers.CharField()
    fallback_url = serializers.SerializerMethodField()

    def get_fallback_url(self, obj):
        request = self.context['request']
        key = self.context['key']
        url = request.build_absolute_uri('/yeah/' + key + '/pay/' + obj.name + '/')
        return url


class CampaignSerializer(serializers.ModelSerializer):
    """
    # TODO: Write docs
    """
    perks = PerkSerializer(many=True)
    payment_methods = serializers.SerializerMethodField()

    def get_payment_methods(self, obj):
        methods = get_payment_methods()
        context = dict(self.context, key=obj.key)
        ser = PaymentMethodSerializer(methods, many=True, context=context)
        return ser.data

    class Meta:
        model = Campaign
        exclude = ['id', ]

class CampaignKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def to_native(self, value):
        return u'{}'.format(Campaign.objects.get(pk=value).key)

    def to_internal_value(self, data):
        if self.queryset is None:
            raise Exception('Writable related fields must include a `queryset` argument')
        try:
            return self.queryset.get(key=data)
        except ObjectDoesNotExist:
            msg = self.error_messages['does_not_exist'] % smart_text(data)
            raise ValidationError(msg)
        except (TypeError, ValueError):
            received = type(data).__name__
            msg = self.error_messages['incorrect_type'] % received
            raise ValidationError(msg)

class PerkSerializer(serializers.ModelSerializer):
    """
    TODO: write docs
    """
    campaign = CampaignKeyRelatedField(queryset=Campaign.objects.all())
    state = serializers.SerializerMethodField()


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
        return(obj.state == Transaction.STATE_OPEN)

    def _get_received(self, obj):
        return(obj.state == Transaction.STATE_COMPLETE)

    def _get_confirmed(self, obj):
        return(obj.state == Transaction.STATE_COMPLETE)

    class Meta:
        model = Transaction
        fields = ('id', 'transaction_id', 'campaign', 'state', 'pledged', 'received', 'confirmed')




    # client_token = serializers.SerializerMethodField()
    #
    # def get_client_token(self, obj):
    #     if obj.module_name != 'yldt_braintree':
    #         return None
    #
    #     request = self.context['request']
    #     key = self.context['key']
    #     return obj.get_client_token()