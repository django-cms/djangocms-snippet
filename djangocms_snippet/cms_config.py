from django.conf import settings

from cms.app_base import CMSAppConfig, CMSAppExtension

from djangocms_versioning.datastructures import VersionableItem, default_copy

from .models import Snippet


class SnippetCMSAppConfig(CMSAppConfig):
    djangocms_versioning_enabled = getattr(
        settings, 'VERSIONING_ALIAS_MODELS_ENABLED', True)

    if djangocms_versioning_enabled:
        versioning = [
            VersionableItem(
                content_model=Snippet,
                grouper_field_name="snippet_grouper",
                copy_function=default_copy,
            )
        ]
