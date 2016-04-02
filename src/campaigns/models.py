#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
import os

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.postgres.fields import HStoreField

from polymorphic.models import PolymorphicModel, PolymorphicManager

# @python_2_unicode_compatible
# class BankAccount(models.Model):
#     user = models.ForeignKey(User)
#     description = models.CharField(max_length=256, blank=True, null=True)
#     btc_address = models.CharField(max_length=1024, blank=True, null=True)
#
#     def __str__(self):
#         if self.description and self.btc_address:
#             return '{} ({})'.format(self.description, self.btc_address)
#         elif not self.description and self.btc_address:
#             return self.btc_address
#         elif self.description and not self.btc_address:
#             return self.description
#         else:
#             return _('Unnamed account')
#from campaigns.payment_method import get_method_by_name
from campaigns.payment_method import get_actions_by_name


def pkgen():
    """
    Generates the primary key codes for the Campaign class.
    """
    while True:
        new_key = base64.urlsafe_b64encode(os.urandom(12))
        # TODO: Filter rude words from generated
        if Campaign.objects.filter(key=new_key).count() == 0:
                return new_key

CURRENCY_EUR = (0, _('EUR'))
CURRENCY_USD = (1, _('USD'))
CURRENCY_BITCOIN = (2, _('BTC'))

CURRENCIES = (
    CURRENCY_EUR,
    CURRENCY_USD,
    CURRENCY_BITCOIN
)


@python_2_unicode_compatible
class Campaign(models.Model):
    """
    Campaign is the central piece of the model.
    """
    CURRENCIES = CURRENCIES
    key = models.CharField(max_length=16, null=True, default=pkgen)
    is_private = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact_info = models.TextField(blank=True)
    currency = models.IntegerField(choices=CURRENCIES)
    goal = models.DecimalField(max_digits=20, decimal_places=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @property
    def state(self):
        try:
            return self.state_of
        except CampaignState.DoesNotExist:
            CampaignState(campaign=self)._super_save()
            return self.state_of

    @property
    def completed(self):
        return self.state.completed

    @property
    def has_started(self):
        return timezone.now() >= self.start_date

    @property
    def days_left(self):
        now = timezone.now()
        if now >= self.end_date:
            return 0

        delta = self.end_date - now
        return delta.days

    def get_total_pledge_amount(self):
        return self.transaction_set.filter(campaign=self,
            state=Transaction.STATE_COMPLETE).aggregate(Sum('amount'))['amount__sum']

    def __str__(self):
        return '{} ({})'.format(self.title, self.key)


@python_2_unicode_compatible
class Perk(models.Model):
    """
    Each campaign can have a number of perks.
    """
    campaign = models.ForeignKey('Campaign', related_name='perks')
    title = models.CharField(max_length=256)
    text = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    available = models.IntegerField(blank=True, null=True)

    @property
    def ui_state(self):
        return 'OK'

    @ui_state.setter
    def ui_state(self, value):
        pass

    @property
    def state(self):
        try:
            return self.state_of
        except PerkState.DoesNotExist:
            PerkState(perk=self)._super_save()
            return self.state_of

    @property
    def is_limited(self):
        return self.available >= 1


    def __str__(self):
        return '{} ({})'.format(self.title, self.amount)


class ReadModel(models.Model):
    """
    The read model is an abstract class for creating read-only models
    that present the state of the system to the outside.
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Disable the save method
        """
        raise NotImplementedError()

    def _super_save(self, *args, **kwargs):
        super(ReadModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Disable the delete method.
        """
        raise NotImplementedError()

    def _super_delete(self, *args, **kwargs):
        super(ReadModel, self).delete(*args, **kwargs)


class CampaignState(ReadModel):
    """
    ReadModel to represent the current state of a Campaign instance.
    """
    campaign = models.OneToOneField('Campaign', related_name='state_of')
    total_received = models.DecimalField(decimal_places=10, max_digits=20, default=0)
    total_pledged = models.DecimalField(decimal_places=10, max_digits=20, default=0)
    total_supporters = models.IntegerField(default=0)
    total_pledgers = models.IntegerField(default=0)

    @property
    def completed(self):
        return self.total_received >= self.campaign.goal

    @property
    def total_incomplete(self):
        return self.total_pledgers - self.total_supporters

    @property
    def percent_funded(self):
        percent = (self.total_received / self.campaign.goal) * 100
        return percent

    @property
    def pending(self):
        return self.total_pledged - self.total_received


class PerkState(ReadModel):
    perk = models.OneToOneField('Perk', related_name='state_of')
    total_pledged = models.IntegerField(default=0)
    total_received = models.IntegerField(default=0)

    @property
    def perks_left(self):
        return self.perk.available - self.total_pledged


class Transaction(ReadModel):
    STATE_PLEDGED    = 0
    STATE_UNVERIFIED = 30
    STATE_VERIFIED   = 60
    STATE_PROCESSING = 100
    STATE_COMPLETE   = 200
    STATE_ABORTED    = 500

    STATES = (
        (STATE_PLEDGED,    _('pledged')),
        (STATE_UNVERIFIED, _('unverified')),
        (STATE_VERIFIED,   _('verified')),
        (STATE_PROCESSING, _('payment processing')),
        (STATE_COMPLETE,   _('complete')),
        (STATE_ABORTED,    _('aborted'))
    )

    # transaction holds the UUID for this transaction
    campaign = models.ForeignKey('Campaign', null=True, blank=True)
    transaction_id = models.CharField(max_length=1024)
    payment_method_name = models.CharField(max_length=1024)
    state = models.IntegerField(choices=STATES)

    amount = models.DecimalField(decimal_places=10, max_digits=20)
    amount_received = models.DecimalField(decimal_places=10, max_digits=20)
    # is_pending = models.BooleanField(default=False)
    started = models.DateTimeField()
    name = models.CharField(max_length=1024, default='')
    email = models.EmailField(null=True, blank=True)
    perk = models.ForeignKey('Perk', null=True, blank=True)
    show_name = models.BooleanField(default=False)

    def get_actions(self):
        return get_actions_by_name(self.payment_method_name, self.transaction_id)


@python_2_unicode_compatible
class BaseEvent(PolymorphicModel):
    """
    Events are simplistic way of keeping a log of all the changes
    in our database.
    """
    created = models.DateTimeField(auto_now_add=True)
    data = HStoreField()

    # queryset_class = HStoreQuerySet
    # event_type = models.IntegerField()
    #
    # # Schema can be overwritten by subclasses
    schema = None
    #
    def reload_schema(self):
        if self.schema != None:
            field = self._meta.get_field('data')
            field.reload_schema(self.schema)

    def __str__(self):
        return '{} - {}: {}'.format(self.__class__.__name__, self.created, self.data)

class BeginPaymentEvent(BaseEvent):
    pass
    # schema = [
    #      {'name': 'transaction_id', 'class': 'CharField', 'kwargs': {'max_length': 36}},
    #      {'name': 'campaign_key', 'class': 'CharField', 'kwargs': {'max_length': 16}},
    #      {'name': 'amount', 'class': 'DecimalField', 'kwargs': {'decimal_places': 8, 'max_digits': 20}},
    # ]

class ReceivePaymentEvent(BaseEvent):
    pass
    # schema = [
    #      {'name': 'transaction_id', 'class': 'CharField', 'kwargs': {'max_length': 36}},
    #      {'name': 'amount', 'class': 'DecimalField', 'kwargs': {'decimal_places': 8, 'max_digits': 20}},
    # ]

class AbortPaymentEvent(BaseEvent):
    pass