# -*- coding: utf-8 -*-

from campaigns.models import *
from django.core.mail import send_mail
from django.template import Context, Template

"""
This module contains the code concerned with sending messages
to users, e.g. payment confirmations.
"""

PAYMENT_CONFIRMATION_TEMPLATE = '''
Dear {{ recipient_name }},

we just received your payment of {{ amount }} earth credit units.

{% if perk %}
    You select the following perk: {{ perk.title }}
{% else %}
    You did not select a perk.
{% endif %}


Yours truly,
Yeah Let's Do That

'''

def render_mail_template(template, variables):
    template = Template(template)
    context = Context(variables)
    return template.render(context)

def send_payment_confirmation(campaign, transaction, template):
    variables = {
        'recipient_address': transaction.email,
        'recipient_name': transaction.name,
        'amount': transaction.amount,
        'perk': transaction.perk
    }
    recipient_address = transaction.email
    message = render_mail_template(template, variables)
    send_mail("Yeah let's confirm that payment", message, 'me@uwekamper.de',
        [recipient_address], fail_silently=False)