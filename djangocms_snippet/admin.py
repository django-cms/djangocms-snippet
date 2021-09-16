from django.conf import settings
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Snippet


try:
    from djangocms_versioning.admin import ExtendedVersionAdminMixin

    djangocms_versioning_installed = True
except ImportError:
    djangocms_versioning_installed = False


class AbstractSnippetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ['slug', 'name']
    prepopulated_fields = {'slug': ('name',)}
    change_form_template = 'djangocms_snippet/admin/change_form.html'
    text_area_attrs = {
        'rows': 20,
        'data-editor': True,
        'data-mode': getattr(settings, 'DJANGOCMS_SNIPPET_THEME', 'html'),
        'data-theme': getattr(settings, 'DJANGOCMS_SNIPPET_MODE', 'github'),
    }

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs=text_area_attrs)}
    }

    class Meta:
        abstract = True



djangocms_versioning_enabled = getattr(
    settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED', False
)

snippet_admin_classes = [
    AbstractSnippetAdmin,
]


if djangocms_versioning_installed and djangocms_versioning_enabled:
    snippet_admin_classes = [ExtendedVersionAdminMixin] + snippet_admin_classes


class SnippetAdmin(*snippet_admin_classes):
    class Meta:
        model = Snippet


admin.site.register(Snippet, SnippetAdmin)
