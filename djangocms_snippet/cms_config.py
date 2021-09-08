from django.conf import settings

from cms.app_base import CMSAppConfig

from .models import Snippet


class SnippetCMSAppConfig(CMSAppConfig):
    djangocms_versioning_enabled = getattr(
        settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED', False
    )

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
