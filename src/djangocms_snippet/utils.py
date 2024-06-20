from cms.toolbar.utils import get_toolbar_from_request
from django.conf import settings

try:
    import djangocms_versioning  # NOQA: F401

    is_versioning_installed = True
except ImportError:
    is_versioning_installed = False

djangocms_versioning_enabled = is_versioning_installed and getattr(
    settings, "DJANGOCMS_SNIPPET_VERSIONING_ENABLED", True
)


def show_draft_content(request=None):
    """
    Returns True if draft contents should be shown.
    """
    if not request:
        return False
    request_toolbar = get_toolbar_from_request(request)
    return request_toolbar.edit_mode_active or getattr(request_toolbar, "preview_mode_active", True)
