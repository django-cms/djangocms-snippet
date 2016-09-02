# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0005_set_related_name_for_cmsplugin_ptr'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='snippetptr',
            options={'verbose_name': 'Snippet', 'verbose_name_plural': 'Snippets'},
        ),
        migrations.AlterField(
            model_name='snippet',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='slug',
            field=models.SlugField(default='', unique=True, max_length=255, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='template',
            field=models.CharField(help_text='Enter a template (i.e. "snippets/plugin_xy.html") which will be rendered. If "template" is given, the contents of field "HTML" will be passed as template variable {{ html }} to the template. Else, the content of "HTML" is rendered.', max_length=255, verbose_name='Template', blank=True),
        ),
    ]
