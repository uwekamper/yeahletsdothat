# -*- coding: utf-8 -*-
from decimal import Decimal
from campaigns.models import Campaign, Transaction, BeginPaymentEvent, \
    ReceivePaymentEvent, AbortPaymentEvent, CampaignState, Perk


class HandlerNotFoundException(Exception):
    pass


projector_pool = []

def register_projector(projector_class):
    projector_pool.append(projector_class)

def handle_event(event):
    for projector_class in projector_pool:
        projector = projector_class()
        projector._handle_event(event)


class Projector(object):
    """
    Abstract projector class. Contains registry.
    """
    def __init__(self):
        self.registry = {}

    def _handle_event(self, event):
        event_type = event.get_real_instance_class()
        try:
            handler_func = self.registry[event_type]
        except KeyError, e:
            # raise HandlerNotFoundException()
            return

        handler_func(event)

    def register(self, event_type, handler_func):
        self.registry[event_type] = handler_func


class TransactionProjector(Projector):
    """
    Project the events to create TransactionState read-models.
    """
    def __init__(self, *args, **kwargs):
        super(TransactionProjector, self).__init__()
        self.register(BeginPaymentEvent, self.handle_begin_payment)
        self.register(ReceivePaymentEvent, self.handle_received_payment)
        self.register(AbortPaymentEvent, self.handle_abort_payment)

    def handle_begin_payment(self, event):
        campaign = Campaign.objects.get(key=event.data['campaign_key'])
        trans = Transaction(
            campaign=campaign,
            transaction_id=event.data['transaction_id'],
            state=Transaction.STATE_OPEN,
            amount=event.data['amount'],
            amount_received=0,
            started=event.created,
            email=event.data['email'],
            name=event.data.get('name', ''),
            show_name=event.data.get('show_name', True),
            payment_method_name=event.data.get('payment_method_name', 'braintree')
        )
        try:
            perk = Perk.objects.get(pk=event.data['perk_id'])
            trans.perk = perk
        except KeyError:
            pass
        except Perk.DoesNotExist:
            pass

        trans._super_save()

    def handle_received_payment(self, event):
        trans = Transaction.objects.get(transaction_id=event.data['transaction_id'])
        trans.amount_received += Decimal(event.data['amount'])
        if trans.amount_received >= trans.amount:
            trans.state = Transaction.STATE_COMPLETE
        trans._super_save()

    def handle_abort_payment(self, event):
        trans = Transaction.objects.get(transaction_id=event.data['transaction_id'])
        trans.state = Transaction.STATE_ABORTED
        trans._super_save()

register_projector(TransactionProjector)

class CampaignStateProjector(Projector):
    """
    Project the events to create TransactionState read-models.
    """
    def __init__(self, *args, **kwargs):
        super(CampaignStateProjector, self).__init__()
        self.register(BeginPaymentEvent, self.handle_begin_payment)
        self.register(ReceivePaymentEvent, self.handle_received_payment)

    def handle_begin_payment(self, event):
        amount = event.data['amount']
        transaction_id = event.data['transaction_id']
        state = Transaction.objects.get(transaction_id=transaction_id).campaign.state
        state.total_pledged += Decimal(amount)
        state.total_pledgers += 1
        state._super_save()

    def handle_received_payment(self, event):
        amount = event.data['amount']
        transaction_id = event.data['transaction_id']
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        state = transaction.campaign.state
        state.total_received += Decimal(amount)
        state.total_supporters += 1
        state._super_save()

register_projector(CampaignStateProjector)

class PerkStateProjector(Projector):
    def __init__(self, *args, **kwargs):
        super(PerkStateProjector, self).__init__()
        self.register(BeginPaymentEvent, self.handle_begin_payment)
        self.register(ReceivePaymentEvent, self.handle_received_payment)

    def handle_begin_payment(self, event):
        perk_id = event.data.get('perk_id', None)
        if perk_id != None:
            perk = Perk.objects.get(pk=perk_id)
            perk.state.total_pledged += 1
            perk.state._super_save()

    def handle_received_payment(self, event):
        transaction_id = event.data['transaction_id']
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        perk = transaction.perk

        if perk != None:
            perk.state.total_received += 1
            perk.state._super_save()


register_projector(PerkStateProjector)
