from django.conf import settings

from cms.app_base import CMSAppConfig

from djangocms_snippet.models import Snippet


try:
    from djangocms_moderation import __version__  # NOQA

    djangocms_moderation_installed = True
except ImportError:
    djangocms_moderation_installed = False


def _get_model_fields(instance, model, field_exclusion_list=[]):
    """
    Iterate over fields excluding
    :param instance:
    :param model:
    :param field_exclusion_list:
    :return:
    """
    field_exclusion_list.append(model._meta.pk.name)
    return {
        field.name: getattr(instance, field.name)
        for field in model._meta.fields
        if field.name not in field_exclusion_list
    }


def snippet_copy_method(old_snippet):
    """
    The most basic copy method, given the model only contains simple foreign key relationships
    :param old_snippet: Old Snippet instance
    :return: New Snippet instance with old instance values (excluding ID)
    """
    return Snippet.objects.create(**_get_model_fields(old_snippet, Snippet))


class SnippetCMSAppConfig(CMSAppConfig):
    djangocms_versioning_enabled = getattr(
        settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED', False
    )
    djangocms_moderation_enabled = getattr(
        settings, 'DJANGOCMS_SNIPPET_MODERATION_ENABLED', False
    )

    if djangocms_moderation_enabled and djangocms_moderation_installed:
        djangocms_moderation_enabled = True
        moderated_models = [Snippet]

    if djangocms_versioning_enabled:
        from djangocms_versioning.datastructures import VersionableItem

        versioning = [
            VersionableItem(
                content_model=Snippet,
                grouper_field_name="snippet_grouper",
                copy_function=snippet_copy_method,
            )
        ]
