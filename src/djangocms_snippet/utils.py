from cms.toolbar.utils import get_toolbar_from_request


def show_draft_content(request=None):
    """
    Returns True if draft contents should be shown.
    """
    if not request:
        return False
    request_toolbar = get_toolbar_from_request(request)
    return request_toolbar.edit_mode_active or request_toolbar.preview_mode_active
