# Generated by Django 5.0.1 on 2024-05-19 21:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_snippet", "0010_alter_snippet_id"),
        ("djangocms_snippet", "0013_snippet_site"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="snippet",
            options={
                "ordering": ["name"],
                "verbose_name": "Snippet",
                "verbose_name_plural": "Snippets",
            },
        ),
        migrations.AlterField(
            model_name="snippet",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="snippet",
            name="slug",
            field=models.SlugField(
                default="", max_length=255, verbose_name="Slug"
            ),
        ),
        migrations.AlterField(
            model_name="snippetgrouper",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
