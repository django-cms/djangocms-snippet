# Generated by Django 4.1.7 on 2023-02-28 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('djangocms_snippet', '0008_auto_change_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippetptr',
            name='cmsplugin_ptr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s', serialize=False, to='cms.cmsplugin'),
        ),
    ]
