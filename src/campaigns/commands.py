# -*- coding: utf-8 -*-

from django.db import transaction
from projectors import handle_event
"""
RULES:
  * commands must only create events
  * commands never change an aggregate model themselves
  * commands never delete events, only add to the event stream.
  * you can of course check the current state of aggregate models
    to validate the input.
"""
from campaigns.models import BeginPaymentEvent, ReceivePaymentEvent, AbortPaymentEvent


class CommandError(Exception):
    pass


def command(command_func):
    """
    Decorator for commands. Applies the events automatically.
    """
    def wrapper(*args, **kwargs):
        handled_events = []
        with transaction.atomic():
            for event in command_func(*args, **kwargs):
                event.save()
            handle_event(event)
            handled_events.append(event)
        return handled_events
    return wrapper

@command
def begin_payment(id, campaign_key, amount, email, perk_id, name, show_name,
                  payment_method_name):
    """
    Begin a payment procedure.
    """
    data = dict(transaction_id=id, campaign_key=campaign_key, amount=amount,
        email=email, perk_id=perk_id, name=name, show_name=show_name,
        payment_method_name=payment_method_name)
    yield BeginPaymentEvent(data=data)

@command
def receive_payment(id, amount):
    """
    Process a payment received for a transaction.
    """
    data = dict(transaction_id=id, amount=amount)
    yield ReceivePaymentEvent(data=data)

@command
def abort_payment(id):
    """
    Stop the payment process for one transaction id.
    """
    data = dict(transaction_id=id)
    yield AbortPaymentEvent(data=data)