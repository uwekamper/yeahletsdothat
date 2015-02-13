# -*- coding: utf-8 -*-
from models import BeginPaymentEvent, TransactionState

class HandlerNotFoundException(Exception):
    pass


class Denormalizer(object):
    """

    """

    def __init__(self):
        self.registry = {}

    def _handle_event(self, event):
        event_type = event.get_event_type()
        try:
            handler_func = self.registry[event_type]
        except KeyError, e:
            raise HandlerNotFoundException()

        handler_func(event)

    def register(self, event_type, handler_func):
        self.registry[event_type] = handler_func


class TransactionDenormalizer(Denormalizer):
    """

    """
    def __init__(self, *args, **kwargs):
        super(TransactionDenormalizer, self).__init__()
        self.register(BeginPaymentEvent, self.handle_begin_payment)
        #self.register(Event.COMPLETE_PAYMENT, self.handle_complete_payment)

    def handle_begin_payment(self, event):
        data = event.data
        trans = TransactionState(
            transaction_id=event.data['id'],
            amount=event.data['amount'],
            is_pending=True,
            started=event.created
        )
        trans._super_save()

    def handle_complete_payment(self, event):
        data = event.data
        trans = TransactionState.objects.get(transaction_id=data['id'])
        trans.is_pending = False
        trans._super_save()
