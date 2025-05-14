from django.db import migrations


def cms4_grouper_version_migration(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Snippet = apps.get_model('djangocms_snippet', 'Snippet')
    SnippetGrouper = apps.get_model('djangocms_snippet', 'SnippetGrouper')

    snippet_queryset = Snippet.objects.using(db_alias).iterator()

    for snippet in snippet_queryset:
        grouper = SnippetGrouper.objects.using(db_alias).create()
        snippet.snippet_grouper = grouper
        snippet.save()


class Migration(migrations.Migration):
    dependencies = [
        ('djangocms_snippet', '0009_auto_20210915_0445'),
    ]

    operations = [
        migrations.RunPython(cms4_grouper_version_migration)
    ]
