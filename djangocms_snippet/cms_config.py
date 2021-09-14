from django.conf import settings

from cms.app_base import CMSAppConfig

from .models import Snippet


def _get_model_fields(instance, model, field_exclusion_list=[]):
    field_exclusion_list.append(model._meta.pk.name)
    return {
        field.name: getattr(instance, field.name)
        for field in model._meta.fields
        if field.name not in field_exclusion_list
    }


def snippet_copy_method(old_snippet):
    old_snippet_fields = _get_model_fields(old_snippet, Snippet)
    import pdb
    pdb.set_trace()
    new_snippet = Snippet.objects.create(**old_snippet_fields)


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
