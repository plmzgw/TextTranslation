# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UploadFile'
        db.create_table(u'autotranslate_uploadfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=50L, null=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('upload_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'autotranslate', ['UploadFile'])

        # Adding model 'TranslatedFile'
        db.create_table(u'autotranslate_translatedfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=50L, null=True)),
            ('trans_lang', self.gf('django.db.models.fields.CharField')(max_length=30L, null=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=100L, null=True)),
            ('trans_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'autotranslate', ['TranslatedFile'])

        # Adding model 'Language'
        db.create_table(u'autotranslate_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=50L, null=True)),
            ('language_chinese', self.gf('django.db.models.fields.CharField')(max_length=50L, null=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=30L, null=True)),
        ))
        db.send_create_signal(u'autotranslate', ['Language'])


    def backwards(self, orm):
        # Deleting model 'UploadFile'
        db.delete_table(u'autotranslate_uploadfile')

        # Deleting model 'TranslatedFile'
        db.delete_table(u'autotranslate_translatedfile')

        # Deleting model 'Language'
        db.delete_table(u'autotranslate_language')


    models = {
        u'autotranslate.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'null': 'True'}),
            'language_chinese': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'null': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '30L', 'null': 'True'})
        },
        u'autotranslate.translatedfile': {
            'Meta': {'object_name': 'TranslatedFile'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'null': 'True'}),
            'trans_lang': ('django.db.models.fields.CharField', [], {'max_length': '30L', 'null': 'True'}),
            'trans_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'autotranslate.uploadfile': {
            'Meta': {'object_name': 'UploadFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['autotranslate']