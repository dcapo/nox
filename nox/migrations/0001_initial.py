# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('asset_dir', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('nox', ['Event'])

        # Adding model 'Invite'
        db.create_table('invite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.CustomUser'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Event'])),
            ('rsvp', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('nox', ['Invite'])

        # Adding model 'TextPost'
        db.create_table('text_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['nox.CustomUser'])),
            ('location', self.gf('geoposition.fields.GeopositionField')(max_length=42)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Event'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('nox', ['TextPost'])

        # Adding model 'ImagePost'
        db.create_table('image_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['nox.CustomUser'])),
            ('location', self.gf('geoposition.fields.GeopositionField')(max_length=42)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Event'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('nox', ['ImagePost'])

        # Adding model 'PlacePost'
        db.create_table('place_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['nox.CustomUser'])),
            ('location', self.gf('geoposition.fields.GeopositionField')(max_length=42)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('venue_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('nox', ['PlacePost'])

        # Adding model 'CustomUser'
        db.create_table('custom_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('nox', ['CustomUser'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('event')

        # Deleting model 'Invite'
        db.delete_table('invite')

        # Deleting model 'TextPost'
        db.delete_table('text_post')

        # Deleting model 'ImagePost'
        db.delete_table('image_post')

        # Deleting model 'PlacePost'
        db.delete_table('place_post')

        # Deleting model 'CustomUser'
        db.delete_table('custom_user')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'nox.event': {
            'Meta': {'object_name': 'Event', 'db_table': "'event'"},
            'asset_dir': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nox.CustomUser']", 'through': "orm['nox.Invite']", 'symmetrical': 'False'})
        },
        'nox.imagepost': {
            'Meta': {'object_name': 'ImagePost', 'db_table': "'image_post'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('geoposition.fields.GeopositionField', [], {'max_length': '42'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nox.CustomUser']"})
        },
        'nox.invite': {
            'Meta': {'object_name': 'Invite', 'db_table': "'invite'"},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rsvp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.CustomUser']"})
        },
        'nox.placepost': {
            'Meta': {'object_name': 'PlacePost', 'db_table': "'place_post'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('geoposition.fields.GeopositionField', [], {'max_length': '42'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nox.CustomUser']"}),
            'venue_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'nox.textpost': {
            'Meta': {'object_name': 'TextPost', 'db_table': "'text_post'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('geoposition.fields.GeopositionField', [], {'max_length': '42'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nox.CustomUser']"})
        }
    }

    complete_apps = ['nox']