#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from campaigns.payment_method import BasePaymentMethod


class BrainTree(BasePaymentMethod):
    name = 'braintree'
    display_name = _('Braintree')

    def pay(self, campaign, transaction):
        url = reverse('yldt_braintree_payment_form', args=(transaction.id, ))
        return HttpResponseRedirect(url)

    def refund(self, campaign, transaction):
        pass