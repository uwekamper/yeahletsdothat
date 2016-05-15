# -*- coding: utf-8 -*-
import pytest
from decimal import Decimal
from django.core import mail

from campaigns import commands
from campaigns.models import Transaction
from campaigns.mailing import send_payment_confirmation, render_mail_template

from .common import campaign


@pytest.mark.django_db(transaction=True)
class TestMailing(object):

    @pytest.fixture
    def transaction_id(self):
        return 'e3ac5128-a8d3-11e4-9f5f-002332c62ffc'

    @pytest.fixture
    def perk_id(self, campaign):
        perk_id = campaign.perks.all()[0].id
        return perk_id

    def test_send_payment_confirmation(self, campaign, transaction_id, perk_id):
        commands.PledgePaymentCommand(transaction_id, campaign.key, Decimal(20),
            'test@example.com', perk_id, "Henner Piffendeckel", False)
        commands.UnverifyPaymentEvent(transaction_id, 'braintree')
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        send_payment_confirmation(campaign, transaction, 'test', 'http://test.de/')

        # Test that one message has been sent.
        assert len(mail.outbox) == 1

        # Verify that the subject of the first message is correct.
        mail.outbox[0].subject == 'Subject here'

    def test_render_mail_template(self):
        test_vars = {'recipient_address': 'test@example.com'}
        test_template = "{{ recipient_address }}."
        result = render_mail_template(test_template, test_vars)
        assert result == 'test@example.com.'