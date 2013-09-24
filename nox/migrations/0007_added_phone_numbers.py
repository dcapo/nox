# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CustomUser.phone_number'
        db.add_column('custom_user', 'phone_number',
                      self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, unique=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CustomUser.phone_number'
        db.delete_column('custom_user', 'phone_number')


    models = {
        'nox.comment': {
            'Meta': {'object_name': 'Comment', 'db_table': "'comment'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nox.CustomUser']"})
        },
        'nox.customuser': {
            'Meta': {'object_name': 'CustomUser', 'db_table': "'custom_user'"},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nox.CustomUser']", 'symmetrical': 'False', 'through': "orm['nox.Invite']", 'blank': 'True'})
        },
        'nox.imagepost': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'ImagePost', 'db_table': "'image_post'", '_ormbases': ['nox.Post']},
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nox.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        'nox.invite': {
            'Meta': {'object_name': 'Invite', 'db_table': "'invite'"},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rsvp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.CustomUser']"})
        },
        'nox.placepost': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'PlacePost', 'db_table': "'place_post'", '_ormbases': ['nox.Post']},
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nox.Post']", 'unique': 'True', 'primary_key': 'True'}),
            'venue_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'nox.post': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Post', 'db_table': "'post'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dislikes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'dislikes'", 'blank': 'True', 'through': "orm['nox.PostDislike']", 'to': "orm['nox.CustomUser']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'likes'", 'blank': 'True', 'through': "orm['nox.PostLike']", 'to': "orm['nox.CustomUser']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['nox.CustomUser']"})
        },
        'nox.postdislike': {
            'Meta': {'object_name': 'PostDislike', 'db_table': "'post_dislike'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.CustomUser']"})
        },
        'nox.postlike': {
            'Meta': {'unique_together': "(('user', 'post'),)", 'object_name': 'PostLike', 'db_table': "'post_like'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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