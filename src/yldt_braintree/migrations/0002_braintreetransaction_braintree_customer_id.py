# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yldt_braintree', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='braintreetransaction',
            name='braintree_customer_id',
            field=models.CharField(default='', max_length=2048),
            preserve_default=False,
        ),
    ]
