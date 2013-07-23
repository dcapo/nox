# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table('post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['nox.CustomUser'])),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Event'])),
        ))
        db.send_create_signal('nox', ['Post'])

        # Deleting field 'Event.asset_dir'
        db.delete_column('event', 'asset_dir')

        # Deleting field 'TextPost.real_type'
        db.delete_column('text_post', 'real_type_id')

        # Deleting field 'TextPost.user'
        db.delete_column('text_post', 'user_id')

        # Deleting field 'TextPost.latitude'
        db.delete_column('text_post', 'latitude')

        # Deleting field 'TextPost.created_at'
        db.delete_column('text_post', 'created_at')

        # Deleting field 'TextPost.event'
        db.delete_column('text_post', 'event_id')

        # Deleting field 'TextPost.longitude'
        db.delete_column('text_post', 'longitude')

        # Deleting field 'TextPost.id'
        db.delete_column('text_post', u'id')

        # Adding field 'TextPost.post_ptr'
        db.add_column('text_post', u'post_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['nox.Post'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'PlacePost.user'
        db.delete_column('place_post', 'user_id')

        # Deleting field 'PlacePost.real_type'
        db.delete_column('place_post', 'real_type_id')

        # Deleting field 'PlacePost.name'
        db.delete_column('place_post', 'name')

        # Deleting field 'PlacePost.latitude'
        db.delete_column('place_post', 'latitude')

        # Deleting field 'PlacePost.created_at'
        db.delete_column('place_post', 'created_at')

        # Deleting field 'PlacePost.event'
        db.delete_column('place_post', 'event_id')

        # Deleting field 'PlacePost.longitude'
        db.delete_column('place_post', 'longitude')

        # Deleting field 'PlacePost.id'
        db.delete_column('place_post', u'id')

        # Adding field 'PlacePost.post_ptr'
        db.add_column('place_post', u'post_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['nox.Post'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ImagePost.real_type'
        db.delete_column('image_post', 'real_type_id')

        # Deleting field 'ImagePost.user'
        db.delete_column('image_post', 'user_id')

        # Deleting field 'ImagePost.latitude'
        db.delete_column('image_post', 'latitude')

        # Deleting field 'ImagePost.created_at'
        db.delete_column('image_post', 'created_at')

        # Deleting field 'ImagePost.event'
        db.delete_column('image_post', 'event_id')

        # Deleting field 'ImagePost.longitude'
        db.delete_column('image_post', 'longitude')

        # Deleting field 'ImagePost.id'
        db.delete_column('image_post', u'id')

        # Adding field 'ImagePost.post_ptr'
        db.add_column('image_post', u'post_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['nox.Post'], unique=True, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table('post')

        # Adding field 'Event.asset_dir'
        db.add_column('event', 'asset_dir',
                      self.gf('django.db.models.fields.CharField')(default='images', max_length=64),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'TextPost.real_type'
        raise RuntimeError("Cannot reverse this migration. 'TextPost.real_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TextPost.user'
        raise RuntimeError("Cannot reverse this migration. 'TextPost.user' and its values cannot be restored.")
        # Adding field 'TextPost.latitude'
        db.add_column('text_post', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'TextPost.created_at'
        raise RuntimeError("Cannot reverse this migration. 'TextPost.created_at' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'TextPost.event'
        raise RuntimeError("Cannot reverse this migration. 'TextPost.event' and its values cannot be restored.")
        # Adding field 'TextPost.longitude'
        db.add_column('text_post', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'TextPost.id'
        raise RuntimeError("Cannot reverse this migration. 'TextPost.id' and its values cannot be restored.")
        # Deleting field 'TextPost.post_ptr'
        db.delete_column('text_post', u'post_ptr_id')


        # User chose to not deal with backwards NULL issues for 'PlacePost.user'
        raise RuntimeError("Cannot reverse this migration. 'PlacePost.user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'PlacePost.real_type'
        raise RuntimeError("Cannot reverse this migration. 'PlacePost.real_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'PlacePost.name'
        raise RuntimeError("Cannot reverse this migration. 'PlacePost.name' and its values cannot be restored.")
        # Adding field 'PlacePost.latitude'
        db.add_column('place_post', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PlacePost.created_at'
        raise RuntimeError("Cannot reverse this migration. 'PlacePost.created_at' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'PlacePost.event'
        raise RuntimeError("Cannot reverse this migration. 'PlacePost.event' and its values cannot be restored.")
        # Adding field 'PlacePost.longitude'
        db.add_column('place_post', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PlacePost.id'
        raise RuntimeError("Cannot reverse this migration. 'PlacePost.id' and its values cannot be restored.")
        # Deleting field 'PlacePost.post_ptr'
        db.delete_column('place_post', u'post_ptr_id')


        # User chose to not deal with backwards NULL issues for 'ImagePost.real_type'
        raise RuntimeError("Cannot reverse this migration. 'ImagePost.real_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ImagePost.user'
        raise RuntimeError("Cannot reverse this migration. 'ImagePost.user' and its values cannot be restored.")
        # Adding field 'ImagePost.latitude'
        db.add_column('image_post', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ImagePost.created_at'
        raise RuntimeError("Cannot reverse this migration. 'ImagePost.created_at' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ImagePost.event'
        raise RuntimeError("Cannot reverse this migration. 'ImagePost.event' and its values cannot be restored.")
        # Adding field 'ImagePost.longitude'
        db.add_column('image_post', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ImagePost.id'
        raise RuntimeError("Cannot reverse this migration. 'ImagePost.id' and its values cannot be restored.")
        # Deleting field 'ImagePost.post_ptr'
        db.delete_column('image_post', u'post_ptr_id')


    models = {
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nox.CustomUser']", 'symmetrical': 'False', 'through': "orm['nox.Invite']", 'blank': 'True'})
        },
        'nox.imagepost': {
            'Meta': {'object_name': 'ImagePost', 'db_table': "'image_post'", '_ormbases': ['nox.Post']},
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
            'Meta': {'object_name': 'PlacePost', 'db_table': "'place_post'", '_ormbases': ['nox.Post']},
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nox.Post']", 'unique': 'True', 'primary_key': 'True'}),
            'venue_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'nox.post': {
            'Meta': {'object_name': 'Post', 'db_table': "'post'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nox.CustomUser']"})
        },
        'nox.textpost': {
            'Meta': {'object_name': 'TextPost', 'db_table': "'text_post'", '_ormbases': ['nox.Post']},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nox.Post']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['nox']