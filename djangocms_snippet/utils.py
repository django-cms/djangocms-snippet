from django.apps import apps


def is_versioning_enabled():
    from .models import Snippet
    try:
        app_config = apps.get_app_config('djangocms_versioning')
        return app_config.cms_extension.is_content_model_versioned(Snippet)
    except LookupError:
        return False
