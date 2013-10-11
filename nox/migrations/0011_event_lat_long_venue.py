# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.longitude'
        db.add_column('event', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)

        # Adding field 'Event.latitude'
        db.add_column('event', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)

        # Adding field 'Event.venue_id'
        db.add_column('event', 'venue_id',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.longitude'
        db.delete_column('event', 'longitude')

        # Deleting field 'Event.latitude'
        db.delete_column('event', 'latitude')

        # Deleting field 'Event.venue_id'
        db.delete_column('event', 'venue_id')


    models = {
        'nox.customuser': {
            'Meta': {'object_name': 'CustomUser', 'db_table': "'custom_user'"},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'unique': 'True', 'null': 'True'})
        },
        'nox.event': {
            'Meta': {'ordering': "['-started_at']", 'object_name': 'Event', 'db_table': "'event'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_events'", 'to': "orm['nox.CustomUser']"}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nox.CustomUser']", 'symmetrical': 'False', 'through': "orm['nox.Invite']", 'blank': 'True'}),
            'venue_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'nox.imagepost': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'ImagePost', 'db_table': "'image_post'", '_ormbases': ['nox.Post']},
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nox.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        'nox.invite': {
            'Meta': {'unique_together': "(('user', 'event'),)", 'object_name': 'Invite', 'db_table': "'invite'"},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rsvp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.CustomUser']"})
        },
        'nox.placepost': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'PlacePost', 'db_table': "'place_post'", '_ormbases': ['nox.Post']},
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nox.Post']", 'unique': 'True', 'primary_key': 'True'}),
            'venue_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'nox.post': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Post', 'db_table': "'post'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'opinions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'opinions'", 'blank': 'True', 'through': "orm['nox.PostOpinion']", 'to': "orm['nox.CustomUser']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['nox.CustomUser']"})
        },
        'nox.postcomment': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'PostComment', 'db_table': "'post_comment'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['nox.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nox.CustomUser']"})
        },
        'nox.postopinion': {
            'Meta': {'unique_together': "(('user', 'post'),)", 'object_name': 'PostOpinion', 'db_table': "'post_opinion'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.CustomUser']"})
        },
        'nox.textpost': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'TextPost', 'db_table': "'text_post'", '_ormbases': ['nox.Post']},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nox.Post']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['nox']