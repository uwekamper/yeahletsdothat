# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from campaigns.payment_method import BasePaymentMethod
from campaigns.models import Transaction
from . import views

class PaymentMethod(BasePaymentMethod):
    """
    Abstract base class for all payment methods
    """
    def pay(self, request, campaign_key, transaction_id):
        """
        Base payment method. We will call this method whenever a payment transaction
        is created.

        Should return a valid HttpResponse instance (e.g. HttpResponseRedirect).
        """
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        campaign = transaction.campaign
        transaction_path = reverse(views.payment_edit, args=[transaction_id])
        context = Context({
            'transaction': transaction,
            'campaign': campaign,
            'transaction_url': request.build_absolute_uri(transaction_path)
        })
        message = get_template('yldt_cash_payment/email_cash_payment.txt').render(context)
        subject = get_template('yldt_cash_payment/email_cash_payment_subject.txt').render(context)
        send_mail(subject, message, 'me@uwekamper.de', [transaction.email])
        imessage = get_template('yldt_cash_payment/email_initiator.txt').render(context)
        send_mail(subject, imessage, 'me@uwekamper.de', [campaign.user.email])

        url = reverse(views.payment_info, args=[transaction_id])
        return HttpResponseRedirect(url)

    def complete(self, campaign_key, transaction_id):
        """
        This method should be called, when the payment was successfully processed.
        It will set the transaction to STATE_PAYMENT_CONFIRMED and send an e-mail to
        the person who payed for the transaction.
        """
        pass

    def refund(self, campaign_key, transaction_id):
        """
        Base payment method. We will call this method whenever a payment transaction
        is created.
        """
        raise NotImplementedError()

    def get_actions(self, transaction_id):
        edit_url = reverse(views.payment_edit, args=[transaction_id])
        return [{'name': _('Edit'), 'url': edit_url}]