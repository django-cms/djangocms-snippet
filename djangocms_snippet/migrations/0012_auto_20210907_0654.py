# Generated by Django 2.2.24 on 2021-09-07 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0011_cms4_plugin_data_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippetptr',
            old_name='new_snippet',
            new_name='snippet_grouper',
        ),
        migrations.RemoveField(
            model_name='snippetptr',
            name='snippet',
        ),
    ]