# Generated by Django 4.2.6 on 2023-10-25 23:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_snippet", "0009_alter_snippetptr_cmsplugin_ptr"),
    ]

    operations = [
        migrations.AlterField(
            model_name="snippet",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
