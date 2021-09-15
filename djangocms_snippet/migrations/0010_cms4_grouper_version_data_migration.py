from django.apps import apps as global_apps
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations

from djangocms_snippet.cms_config import SnippetCMSAppConfig
from djangocms_snippet.conf import (
    DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID,
)


try:
    from djangocms_versioning.constants import DRAFT

    djangocms_versioning_installed = True
except ImportError:
    djangocms_versioning_installed = False


def cms4_grouper_version_migration(apps, schema_editor):
    create_contenttypes(global_apps.get_app_config("djangocms_snippet"))

    djangocms_versioning_config_enabled = SnippetCMSAppConfig.djangocms_versioning_enabled

    ContentType = apps.get_model('contenttypes', 'ContentType')
    Snippet = apps.get_model('djangocms_snippet', 'Snippet')
    SnippetGrouper = apps.get_model('djangocms_snippet', 'SnippetGrouper')
    User = apps.get_model('auth', 'User')

    snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')
    snippet_queryset = Snippet.objects.all()

    for snippet in snippet_queryset:
        grouper = SnippetGrouper.objects.create()
        snippet.snippet_grouper = grouper
        snippet.save()

        # Get a migration user.
        migration_user = User.objects.get(id=DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID)

        # Create initial Snippet Versions if versioning is enabled and installed.
        if djangocms_versioning_config_enabled and djangocms_versioning_installed:
            Version = apps.get_model('djangocms_versioning', 'Version')
            Version.objects.create(
                created_by=migration_user,
                state=DRAFT,
                number=1,
                object_id=snippet.pk,
                content_type=snippet_contenttype,
            )


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0034_remove_pagecontent_placeholders'),  # Run after the CMS4 migrations
        ('djangocms_snippet', '0009_auto_20210915_0445'),
    ]

    if djangocms_versioning_installed:
        dependencies += [('djangocms_versioning', '0015_version_modified'), ]

    operations = [
        migrations.RunPython(cms4_grouper_version_migration)
    ]
