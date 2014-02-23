# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Activity.max_people'
        db.alter_column(u'activities_activity', 'max_people', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Activity.max_people'
        raise RuntimeError("Cannot reverse this migration. 'Activity.max_people' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Activity.max_people'
        db.alter_column(u'activities_activity', 'max_people', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'activities.activity': {
            'Meta': {'object_name': 'Activity'},
            'currency': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'goal': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_people': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_people': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pledge_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'activities.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['activities']