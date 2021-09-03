# Generated by Django 2.2.24 on 2021-08-31 10:45
import logging
from django.apps import apps
from django.db import migrations

from cms.plugin_pool import plugin_pool

from djangocms_snippet.cms_plugins import SnippetPlugin

logger = logging.getLogger(__name__)


def _create_plugin(old_plugin, grouper, Plugin):
    # Create the new plugin
    parent_id = None
    if old_plugin.parent:
        parent_id = old_plugin.parent

    plugin_base = Plugin(
        plugin_type=SnippetPlugin,
        placeholder=old_plugin.placeholder,
        position=1,
        language="en",
        parent_id=parent_id,
    )

    try:
        plugin_model = plugin_pool.get_plugin("SnippetPlugin").model
    except KeyError:
        raise TypeError(
            'plugin_type must be CMSPluginBase subclass or string'
        )

    plugin_base = old_plugin.placeholder.add_plugin(plugin_base)

    old_plugin_position = old_plugin.position
    old_plugin_id = old_plugin.id

    plugin_base.position = old_plugin_position
    plugin = plugin_model({"snippet": old_plugin.snippet, "new_snippet": grouper})
    plugin_base.set_base_attr(plugin)

    if plugin_base:
        logger.info(f"Deleting CMS3 Plugin: {old_plugin_id}")
        old_plugin.cmsplugin_ptr_id = old_plugin.cmsplugin_ptr
        old_plugin.delete()
    plugin_base.save()

    logger.info(
        f"Created CMS4 Snippet plugin: {type(plugin)}-{plugin.id}, for CMS3 plugin: {old_plugin_id}"
    )


def create_groupers(snippet, grouper_model):
    grouper = grouper_model.objects.create()
    snippet.snippet_grouper = grouper
    snippet.save()
    logger.info("Created Snippet Grouper")


def cms4_migration(apps, schema_editor):
    grouper_count = 0
    plugin_count = 0
    Snippet = apps.get_model("djangocms_snippet", "Snippet")
    SnippetGrouper = apps.get_model("djangocms_snippet", "SnippetGrouper")
    SnippetPtr = apps.get_model("djangocms_snippet", "SnippetPtr")
    Plugin = apps.get_model('cms', 'CMSPlugin')
    Placeholder = apps.get_model('cms', 'Placeholder')

    # Iterate over the queryset, create a grouper for each instance which doesn't have one
    # and map the content objects foreign key field to it.
    for snippet in Snippet.objects.all():
        if not snippet.snippet_grouper:
            create_groupers(snippet, SnippetGrouper)
            grouper_count += 1

    logger.info(f"SnippetPlugin count pre-migration: {SnippetPtr.objects.all().count()}")
    # Iterate over the plugin queryset, and replace them each with a CMS4 plugin
    for snippet_plugin in SnippetPtr.objects.all():
        _create_plugin(snippet_plugin, snippet_plugin.snippet, SnippetPtr)
        plugin_count += 1

    logger.info(f"Migration completed, created {grouper_count} Snippet Groupers and {plugin_count} Snippet plugins")


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0009_auto_20210831_0715'),
    ]

    operations = [
        migrations.RunPython(cms4_migration)
    ]
