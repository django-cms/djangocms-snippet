# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0006_auto_20160831_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='template',
            field=models.CharField(help_text='Enter a template (e.g. "snippets/plugin_xy.html") to be rendered. If "template" is given, the contents of field "HTML" will be passed as template variable {{ html }} to the template. Otherwise, the content of "HTML" is rendered.', max_length=255, verbose_name='Template', blank=True),
        ),
    ]
