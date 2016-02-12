#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.encoding import smart_text

from rest_framework import serializers
from campaigns.models import Transaction, Campaign, Perk
from campaigns.templatetags.campaigns_extras import markdown_render
from campaigns.utils import get_payment_methods


class MarkdownField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, obj):
        return markdown_render(obj)

    def to_internal_value(self, value):
        return value


class PaymentPOSTData(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    name = serializers.CharField()
    payment_nonce = serializers.CharField()



class UIStateField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, obj):
        return 'OK'

    def to_internal_value(self, value):
        return value

class NestedPerkSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    text = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    available = serializers.IntegerField()
    ui_state = UIStateField(default='OK', allow_null=True, read_only=False)



class PerkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ui_state = UIStateField(default='OK', source='state', read_only=False)

    def get_ui_state(self, obj):
        return 'OK'

    def update(self, instance, validated_data):
        return instance

    class Meta:
        model = Perk
        fields = ['id', 'title', 'text', 'amount', 'available', 'ui_state']
        # exclude = ['campaign',]


class PaymentMethodSerializer(serializers.Serializer):
    """

    """
    module_name = serializers.CharField()
    name = serializers.CharField()
    fallback_url = serializers.SerializerMethodField()

    def get_fallback_url(self, obj):
        # request = self.context['request']
        key = self.context['key']
        url = '/yeah/' + key + '/pay/' + obj.name + '/'
        return url


class CampaignSerializer(serializers.ModelSerializer):
    """
    # TODO: Write docs
    """
    perks = NestedPerkSerializer(many=True)
    # payment_methods = serializers.SerializerMethodField(read_only=True)
    currency = serializers.CharField(source='get_currency_display')
    description = serializers.CharField(required=True)
    username = serializers.CharField(source='user.username', required=False, read_only=True)
    completed = serializers.BooleanField(source='state.completed', read_only=True)
    percent_funded = serializers.FloatField(source='state.percent_funded', read_only=True)

    def get_payment_methods(self, obj):
        methods = get_payment_methods()
        context = dict(self.context, key=obj.key)
        ser = PaymentMethodSerializer(methods, many=True, context=context)
        return ser.data

    def update(self, instance, validated_data):
        perks_data = validated_data.pop('perks')
        instance = super(CampaignSerializer, self).update(instance, validated_data)
        for perk_data in perks_data:
            perk_id = perk_data.get('id', None)
            if perk_id != None:
                perk = instance.perks.get(pk=perk_data['id'])
                new_state = perk_data.get('ui_state', 'OK')
                if new_state == 'DELETED':
                    perk.delete()
                else:
                    perk.title = perk_data.get('title')
                    perk.text = perk_data.get('text')
                    perk.amount = perk_data.get('amount', 0)
                    perk.available = perk_data.get('available', 0)
                    perk.save()
            else:
                Perk.objects.create(campaign=instance, **perk_data)
        return instance

    class Meta:
        model = Campaign
        exclude = ['id', 'user', ]
        depth = 1

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
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    name = serializers.SerializerMethodField()
    payment_nonce = serializers.SerializerMethodField()

    def get_payment_nonce(self, obj):
        return None

    def get_name(self, obj):
        return "braintree"

    def _get_pledged(self, obj):
        return(obj.state == Transaction.STATE_PLEDGED)

    def _get_received(self, obj):
        return(obj.state == Transaction.STATE_COMPLETE)

    def _get_confirmed(self, obj):
        return(obj.state == Transaction.STATE_COMPLETE)

    class Meta:
        model = Transaction
        fields = ('id', 'transaction_id', 'name', 'amount', 'campaign', 'state', 'pledged',
            'received', 'confirmed', 'payment_nonce')




    # client_token = serializers.SerializerMethodField()
    #
    # def get_client_token(self, obj):
    #     if obj.module_name != 'yldt_braintree':
    #         return None
    #
    #     request = self.context['request']
    #     key = self.context['key']
    #     return obj.get_client_token()