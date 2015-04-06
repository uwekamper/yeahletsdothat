# -*- coding: utf-8 -*-
from django.core.mail import send_mail

from django.db import transaction
from projectors import handle_event
from campaigns.models import BeginPaymentEvent, ReceivePaymentEvent, AbortPaymentEvent, Transaction
from campaigns.mailing import send_payment_confirmation, PAYMENT_CONFIRMATION_TEMPLATE

"""
RULES:
  * commands must only create events
  * commands never change an aggregate model themselves
  * commands never delete events, only add to the event stream.
  * you can of course check the current state of aggregate models
    to validate the input.
"""


class CommandError(Exception):
    pass


class Command(object):
    """
    Base class for commands
    """
    def __init__(self):
        self._handle()

    def pre(self):
        """
        Overwrite this method to implement a pre-hook for a command.
        """
        pass

    def main(self):
        """
        This method will always be replaced with a function
        """
        raise NotImplementedError()

    def post(self):
        """
        Overwrite this method to implement a post-hook for a command.
        """
        pass

    def _handle(self):
        self.pre()
        with transaction.atomic():
            for event in self.main():
                event.save()
                handle_event(event)
        self.post()


class BeginPayment(Command):
    """
    Begin a payment procedure.
    """
    def __init__(self, id, campaign_key, amount, email, perk_id, name, show_name,
                 payment_method_name):
        self.data = dict(
            transaction_id=id,
            campaign_key=campaign_key,
            amount=amount,
            email=email,
            perk_id=perk_id,
            name=name,
            show_name=show_name,
            payment_method_name=payment_method_name
        )
        super(BeginPayment, self).__init__()

    def main(self):
        yield BeginPaymentEvent(data=self.data)


class ReceivePayment(Command):
    """
    Process a payment received for a transaction.
    """
    def __init__(self, id, amount):
        self.transaction_id = id
        self.amount = amount
        super(ReceivePayment, self).__init__()

    def main(self):
        self.data = dict(transaction_id=self.transaction_id, amount=self.amount)
        yield ReceivePaymentEvent(data=self.data)

    def post(self):
        transaction = Transaction.objects.get(transaction_id=self.transaction_id)

        # send an email when the received amount is high enough
        if transaction.amount_received >= transaction.amount:
            campaign = transaction.campaign
            template = PAYMENT_CONFIRMATION_TEMPLATE
            send_payment_confirmation(campaign, transaction, template)

class AbortPayment(Command):
    """
    Stop the payment process for one transaction id.
    """
    def __init__(self, id):
        self.id = id
        super(AbortPayment, self).__init__()

    def main(self):
        data = dict(transaction_id=id)
        yield AbortPaymentEvent(data=data)