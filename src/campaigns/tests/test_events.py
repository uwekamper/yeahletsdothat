# -*- coding: utf-8 -*-

from model_mommy import mommy
import pytest
from campaigns.denormalizers import TransactionDenormalizer
from common import *
import uuid
from django.utils import timezone
from campaigns.models import *
pytestmark = pytest.mark.django_db

"""
Check if everything connected to events and event sourcing (projections,
denormalization, etc.) works as intended.
"""

class TestTransactionDenormalizer(object):
    """

    """
    def test_handle_begin_payment_event(self):
        id = 'e3ac5128-a8d3-11e4-9f5f-002332c62ffc'
        started = timezone.now()
        campaign = Campaign.objects.create(title='TestCampaign', currency=0,
            goal='20.0', start_date=timezone.now(), end_date=timezone.now())
        ev = BeginPaymentEvent.create(id, campaign.key, 23.0)
        ev.save()
        denorm = TransactionDenormalizer()
        denorm._handle_event(ev)

        assert TransactionState.objects.filter(transaction_id=id).exists()
        t = TransactionState.objects.filter(transaction_id=id).first()
        assert t.amount == 23.0
        assert t.started == ev.created
        assert t.is_pending == True

    # def test_handle_complete_payment(self):
    #     self.test_handle_begin_payment_event()
    #
    #     id = 'e3ac5128-a8d3-11e4-9f5f-002332c62ffc'
    #     t = TransactionState.objects.get(transaction_id=id)
    #     assert t.is_pending == True
    #
    #     now = timezone.now()
    #     ev = CompletePaymentEvent({'id': id, 'completed': str(now)})
    #     denorm = TransactionDenormalizer()
    #     denorm._handle_event(ev)
    #
    #     t = TransactionState.objects.get(transaction_id=id)
    #     assert t.is_pending == False

