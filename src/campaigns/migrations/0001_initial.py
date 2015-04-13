# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import campaigns.models
import django.contrib.postgres.fields.hstore
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=campaigns.models.pkgen, max_length=16, null=True)),
                ('is_private', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('contact_info', models.TextField(blank=True)),
                ('currency', models.IntegerField(choices=[(0, 'EUR'), (1, 'USD'), (2, 'BTC')])),
                ('goal', models.DecimalField(max_digits=20, decimal_places=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_received', models.DecimalField(default=0, max_digits=20, decimal_places=10)),
                ('total_pledged', models.DecimalField(default=0, max_digits=20, decimal_places=10)),
                ('total_supporters', models.IntegerField(default=0)),
                ('total_pledgers', models.IntegerField(default=0)),
                ('campaign', models.OneToOneField(related_name='state_of', to='campaigns.Campaign')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Perk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField(null=True, blank=True)),
                ('amount', models.DecimalField(max_digits=20, decimal_places=8)),
                ('available', models.IntegerField(null=True, blank=True)),
                ('campaign', models.ForeignKey(related_name='perks', to='campaigns.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='PerkState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_pledged', models.IntegerField(default=0)),
                ('total_received', models.IntegerField(default=0)),
                ('perk', models.OneToOneField(related_name='state_of', to='campaigns.Perk')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(max_length=1024)),
                ('payment_method_name', models.CharField(max_length=1024)),
                ('state', models.IntegerField(choices=[(0, 'open'), (200, 'complete'), (500, 'aborted')])),
                ('amount', models.DecimalField(max_digits=20, decimal_places=10)),
                ('amount_received', models.DecimalField(max_digits=20, decimal_places=10)),
                ('started', models.DateTimeField()),
                ('name', models.CharField(default='', max_length=1024)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('show_name', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(blank=True, to='campaigns.Campaign', null=True)),
                ('perk', models.ForeignKey(blank=True, to='campaigns.Perk', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AbortPaymentEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='campaigns.BaseEvent')),
            ],
            options={
                'abstract': False,
            },
            bases=('campaigns.baseevent',),
        ),
        migrations.CreateModel(
            name='BeginPaymentEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='campaigns.BaseEvent')),
            ],
            options={
                'abstract': False,
            },
            bases=('campaigns.baseevent',),
        ),
        migrations.CreateModel(
            name='ReceivePaymentEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='campaigns.BaseEvent')),
            ],
            options={
                'abstract': False,
            },
            bases=('campaigns.baseevent',),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_campaigns.baseevent_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
