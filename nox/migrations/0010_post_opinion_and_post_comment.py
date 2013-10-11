# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PostLike', fields ['user', 'post']
        db.delete_unique('post_like', ['user_id', 'post_id'])

        # Removing unique constraint on 'PostDislike', fields ['user', 'post']
        db.delete_unique('post_dislike', ['user_id', 'post_id'])

        # Deleting model 'PostDislike'
        db.delete_table('post_dislike')

        # Deleting model 'PostLike'
        db.delete_table('post_like')

        # Deleting model 'Comment'
        db.delete_table('comment')

        # Adding model 'PostOpinion'
        db.create_table('post_opinion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.CustomUser'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Post'])),
            ('opinion', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('nox', ['PostOpinion'])

        # Adding unique constraint on 'PostOpinion', fields ['user', 'post']
        db.create_unique('post_opinion', ['user_id', 'post_id'])

        # Adding model 'PostComment'
        db.create_table('post_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Post'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['nox.CustomUser'])),
        ))
        db.send_create_signal('nox', ['PostComment'])


    def backwards(self, orm):
        # Removing unique constraint on 'PostOpinion', fields ['user', 'post']
        db.delete_unique('post_opinion', ['user_id', 'post_id'])

        # Adding model 'PostDislike'
        db.create_table('post_dislike', (
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Post'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.CustomUser'])),
        ))
        db.send_create_signal('nox', ['PostDislike'])

        # Adding unique constraint on 'PostDislike', fields ['user', 'post']
        db.create_unique('post_dislike', ['user_id', 'post_id'])

        # Adding model 'PostLike'
        db.create_table('post_like', (
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Post'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.CustomUser'])),
        ))
        db.send_create_signal('nox', ['PostLike'])

        # Adding unique constraint on 'PostLike', fields ['user', 'post']
        db.create_unique('post_like', ['user_id', 'post_id'])

        # Adding model 'Comment'
        db.create_table('comment', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nox.Post'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['nox.CustomUser'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6)),
        ))
        db.send_create_signal('nox', ['Comment'])

        # Deleting model 'PostOpinion'
        db.delete_table('post_opinion')

        # Deleting model 'PostComment'
        db.delete_table('post_comment')


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
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nox.Post']"}),
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