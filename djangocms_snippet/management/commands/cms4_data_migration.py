import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from cms.api import add_plugin

from djangocms_snippet.cms_plugins import SnippetPtrPlugin
from djangocms_snippet.models import Snippet, SnippetGrouper, SnippetPtr
from djangocms_versioning.constants import DRAFT
from djangocms_versioning.models import Version


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command to migrate cms3 model structure into cms4 by creating relevant Groupers and Versions'

    def _create_version(self, snippet, state=DRAFT, number=1):
        # Get a migration user.
        migration_user = getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID", None)
        if not migration_user:
            logger.warning(
                "Setting DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID not provided, defaulting to user id: 1"
            )
            migration_user = User.objects.get(id=1)

        # The contenttype of the content model
        snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')

        logger.info("Creating version for new grouper: {}".format(snippet.pk))
        # Create a new version for the snippet
        Version.objects.create(
            created_by=migration_user,
            state=state,
            number=number,
            object_id=snippet.pk,
            content_type=snippet_contenttype,
        )

    def _create_plugin(self, old_plugin, grouper):
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

    def handle(self, *args, **options):
        # The queryset of populated models.
        queryset = Snippet._base_manager.all()
        # The plugin queryset
        plugin_queryset = SnippetPtr.objects.all()

        # Since we are doing a database migration, use an atomic transaction
        with transaction.atomic():
            version_count = 0
            grouper_count = 0
            plugin_count = 0
            # Iterate over the queryset, create a grouper for each instance which doesn't have one
            # and map the content objects foreign key field to it.
            for snippet in queryset:
                if not snippet.snippet_grouper:
                    grouper = SnippetGrouper.objects.create()
                    snippet.snippet_grouper = grouper
                    snippet.save()
                    logger.info("Created Snippet Grouper")
                    grouper_count += 1
                    # If there are no versions of this content, create one.
                if hasattr(snippet, "versions"):
                    if not snippet.versions.all():
                        self._create_version(snippet=snippet)
                        version_count += 1

            # Iterate over the plugin queryset, and create a new CMS4 plugin for every CMS3 plugin,
            # then delete the old CMS3 plugin
            for plugin in plugin_queryset:
                self._create_plugin(plugin, snippet.snippet_grouper)
                plugin_count += 1

        logger.info(
            f'''Created {version_count} version objects, {grouper_count}''' +
            f'''Snippet grouper objects and {plugin_count} snippet plugins'''
        )
