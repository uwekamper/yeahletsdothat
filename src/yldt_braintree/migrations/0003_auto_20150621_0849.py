# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yldt_braintree', '0002_braintreetransaction_braintree_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='braintreetransaction',
            name='braintree_customer_id',
            field=models.CharField(max_length=2048, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='braintreetransaction',
            name='braintree_transaction_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
