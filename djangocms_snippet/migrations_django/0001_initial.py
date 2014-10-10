# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name')),
                ('html', models.TextField(verbose_name='HTML', blank=True)),
                ('template', models.CharField(help_text='Enter a template (i.e. "snippets/plugin_xy.html") which will be rendered. If "template" is given, the contents of field "HTML" will be passed as template variable {{ html }} to the template. Else, the content of "HTML" is rendered.', max_length=50, verbose_name='template', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Snippet',
                'verbose_name_plural': 'Snippets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnippetPtr',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('snippet', models.ForeignKey(to='djangocms_snippet.Snippet')),
            ],
            options={
                'verbose_name': 'Snippet',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
