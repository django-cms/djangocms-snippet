from django.apps import apps as global_apps
from django.conf import settings
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations


try:
    from djangocms_versioning.constants import DRAFT, PUBLISHED

    djangocms_versioning_installed = True
except ImportError:
    djangocms_versioning_installed = False

djangocms_versioning_config_enabled = getattr(
    settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED', True
)


def cms4_grouper_version_migration(apps, schema_editor):
    create_contenttypes(global_apps.get_app_config("djangocms_snippet"))



    ContentType = apps.get_model('contenttypes', 'ContentType')
    Snippet = apps.get_model('djangocms_snippet', 'Snippet')
    SnippetGrouper = apps.get_model('djangocms_snippet', 'SnippetGrouper')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')
    snippet_queryset = Snippet.objects.all()

    # Get a migration user to create a version.
    if djangocms_versioning_config_enabled and djangocms_versioning_installed and len(snippet_queryset):
        Version = apps.get_model('djangocms_versioning', 'Version')
        migration_user = User.objects.get(id=getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID", 1))

    for snippet in snippet_queryset:
        grouper = SnippetGrouper.objects.create()
        snippet.snippet_grouper = grouper
        snippet.save()

        # Create initial Snippet Versions if versioning is enabled and installed.
        # Publish the snippet because all snippets were assumed published before
        if djangocms_versioning_config_enabled and djangocms_versioning_installed:
            Version.objects.create(
                created_by=migration_user,
                state=PUBLISHED,
                number=1,
                object_id=snippet.pk,
                content_type=snippet_contenttype,
            )


class Migration(migrations.Migration):
    dependencies = [
        # ('cms', '0034_remove_pagecontent_placeholders'),  # Run after the CMS4 migrations
        ('djangocms_snippet', '0009_auto_20210915_0445'),
    ]

    if djangocms_versioning_installed:
        dependencies += [('djangocms_versioning', '0015_version_modified'), ]

    operations = [
        migrations.RunPython(cms4_grouper_version_migration)
    ]
