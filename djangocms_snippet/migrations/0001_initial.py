# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models, connection


class Migration(SchemaMigration):

    def forwards(self, orm):
        table_names = connection.introspection.table_names()
        if 'snippet_snippet' in table_names or 'cmsplugin_snippetptr' in table_names:
            if 'cmsplugin_snippetptr' in table_names:
                db.rename_table('cmsplugin_snippetptr', 'djangocms_snippet_snippetptr')
            if 'snippet_snippet' in table_names:
                db.rename_table('snippet_snippet', 'djangocms_snippet_snippet')
        else:
            # Adding model 'Snippet'
            db.create_table(u'djangocms_snippet_snippet', (
                (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
                ('html', self.gf('django.db.models.fields.TextField')(blank=True)),
                ('template', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ))
            db.send_create_signal(u'djangocms_snippet', ['Snippet'])

            # Adding model 'SnippetPtr'
            db.create_table(u'djangocms_snippet_snippetptr', (
                (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
                ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djangocms_snippet.Snippet'])),
            ))
            db.send_create_signal(u'djangocms_snippet', ['SnippetPtr'])

    def backwards(self, orm):
        # Deleting model 'Snippet'
        db.delete_table(u'djangocms_snippet_snippet')

        # Deleting model 'SnippetPtr'
        db.delete_table(u'djangocms_snippet_snippetptr')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'djangocms_snippet.snippet': {
            'Meta': {'ordering': "['name']", 'object_name': 'Snippet'},
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'djangocms_snippet.snippetptr': {
            'Meta': {'object_name': 'SnippetPtr', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djangocms_snippet.Snippet']"})
        }
    }

    complete_apps = ['djangocms_snippet']