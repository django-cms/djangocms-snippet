from cms.app_base import CMSAppConfig, CMSAppExtension

from djangocms_versioning.datastructures import VersionableItem, default_copy

from .models import Snippet


class SnippetCMSAppConfig(CMSAppConfig):
    djangocms_versioning_enabled = True

    versioning = [
        VersionableItem(
            content_model=Snippet,
            grouper_field_name="snippet_grouper",
            copy_function=default_copy,
        )
    ]
