from django.conf import settings

from cms.app_base import CMSAppConfig

from djangocms_snippet.models import Snippet


try:
    from djangocms_moderation import __version__  # NOQA

    djangocms_moderation_installed = True
except ImportError:
    djangocms_moderation_installed = False


class SnippetCMSAppConfig(CMSAppConfig):
    djangocms_versioning_enabled = getattr(
        settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED', False
    )
    djangocms_moderation_enabled = getattr(
        settings, 'DJANGOCMS_SNIPPET_MODERATION_ENABLED', False
    )

    if djangocms_moderation_enabled and djangocms_moderation_installed:
        moderated_models = [Snippet]

    if djangocms_versioning_enabled:
        from djangocms_versioning.datastructures import (
            VersionableItem, default_copy,
        )

        versioning = [
            VersionableItem(
                content_model=Snippet,
                grouper_field_name="snippet_grouper",
                copy_function=default_copy,
            )
        ]
