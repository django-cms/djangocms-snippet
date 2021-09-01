# Generated by Django 2.2.24 on 2021-08-31 10:45
import logging
from django.db import migrations

from cms.api import add_plugin

from djangocms_snippet.cms_plugins import SnippetPtrPlugin

logger = logging.getLogger(__name__)


def _create_plugin(old_plugin, grouper):
    # Create the new plugin
    new_plugin = add_plugin(
        old_plugin.placeholder,
        plugin_type=SnippetPtrPlugin,
        language="en",
        snippet=old_plugin.snippet,
        new_snippet=grouper,
    )
    old_plugin_position = old_plugin.position
    old_plugin_id = old_plugin.id

    if new_plugin:
        logger.info(f"Deleting CMS3 Plugin: {old_plugin_id}")
        old_plugin.cmsplugin_ptr_id = old_plugin.cmsplugin_ptr
        old_plugin.delete()

    new_plugin.position = old_plugin_position
    logger.info(
        f"Created CMS4 Snippet plugin: {type(new_plugin)}-{new_plugin.id}, for CMS3 plugin: {old_plugin_id}"
    )


def create_groupers(snippet, grouper_model):
    grouper = grouper_model.model.objects.create()
    snippet.snippet_grouper = grouper
    snippet.save()
    logger.info("Created Snippet Grouper")


def cms4_migration(apps, schema_editor):
    grouper_count = 0
    plugin_count = 0
    Snippet = apps.get_model("djangocms_snippet", "Snippet")
    SnippetGrouper = apps.get_model("djangocms_snippet", "SnippetGrouper")
    SnippetPtr = apps.get_model("djangocms_snippet", "SnippetPtr")

    # Iterate over the queryset, create a grouper for each instance which doesn't have one
    # and map the content objects foreign key field to it.
    for snippet in Snippet.objects.all():
        if not snippet.snippet_grouper:
            create_groupers(snippet, SnippetGrouper)
            grouper_count += 1

    logger.info(f"SnippetPlugin count pre-migration: {SnippetPtr.objects.all().count()}")
    # Iterate over the plugin queryset, and replace them each with a CMS4 plugin
    for snippet in SnippetPtr.objects.all():
        _create_plugin(snippet, snippet.snippet_grouper)
        plugin_count += 1

    logger.info(f"Migration completed, created {grouper_count} Snippet Groupers and {plugin_count} Snippet plugins")


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0009_auto_20210831_0715'),
    ]

    operations = [
        migrations.RunPython(cms4_migration)
    ]
