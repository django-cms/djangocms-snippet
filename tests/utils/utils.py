from djangocms_snippet.cms_config import SnippetCMSAppConfig


try:
    from djangocms_versioning import __version__  # NOQA
    versioning_installed = True
except ImportError:
    versioning_installed = False


def is_versioning_enabled():
    if SnippetCMSAppConfig.djangocms_versioning_enabled and versioning_installed:
        return True
    else:
        return False
