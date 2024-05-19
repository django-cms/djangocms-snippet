from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SnippetConfig(AppConfig):
    name = 'djangocms_snippet'
    verbose_name = _('Snippets')
    default_auto_field = 'django.db.models.AutoField'
