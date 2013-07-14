# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TextPost.location'
        db.delete_column('text_post', 'location')

        # Adding field 'TextPost.longitude'
        db.add_column('text_post', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)

        # Adding field 'TextPost.latitude'
        db.add_column('text_post', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)

        # Deleting field 'PlacePost.location'
        db.delete_column('place_post', 'location')

        # Adding field 'PlacePost.longitude'
        db.add_column('place_post', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)

        # Adding field 'PlacePost.latitude'
        db.add_column('place_post', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)

        # Deleting field 'ImagePost.location'
        db.delete_column('image_post', 'location')

        # Adding field 'ImagePost.longitude'
        db.add_column('image_post', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)

        # Adding field 'ImagePost.latitude'
        db.add_column('image_post', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'TextPost.location'
        db.add_column('text_post', 'location',
                      self.gf('geoposition.fields.GeopositionField')(default=0, max_length=42),
                      keep_default=False)

        # Deleting field 'TextPost.longitude'
        db.delete_column('text_post', 'longitude')

        # Deleting field 'TextPost.latitude'
        db.delete_column('text_post', 'latitude')

        # Adding field 'PlacePost.location'
        db.add_column('place_post', 'location',
                      self.gf('geoposition.fields.GeopositionField')(default=0, max_length=42),
                      keep_default=False)

        # Deleting field 'PlacePost.longitude'
        db.delete_column('place_post', 'longitude')

        # Deleting field 'PlacePost.latitude'
        db.delete_column('place_post', 'latitude')

        # Adding field 'ImagePost.location'
        db.add_column('image_post', 'location',
                      self.gf('geoposition.fields.GeopositionField')(default=0, max_length=42),
                      keep_default=False)

        # Deleting field 'ImagePost.longitude'
        db.delete_column('image_post', 'longitude')

        # Deleting field 'ImagePost.latitude'
        db.delete_column('image_post', 'latitude')


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
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
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
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
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
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nox.CustomUser']"})
        }
    }

    complete_apps = ['nox']