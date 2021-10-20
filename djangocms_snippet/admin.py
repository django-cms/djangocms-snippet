from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .cms_config import SnippetCMSAppConfig
from .forms import SnippetForm
from .models import Snippet
from .views import SnippetPreviewView


# Use the version mixin if djangocms-versioning is installed and enabled
snippet_admin_classes = [admin.ModelAdmin]
djangocms_versioning_enabled = SnippetCMSAppConfig.djangocms_versioning_enabled

try:
    from djangocms_versioning.admin import ExtendedVersionAdminMixin

    if djangocms_versioning_enabled:
        snippet_admin_classes.insert(0, ExtendedVersionAdminMixin)
except ImportError:
    pass


class SnippetAdmin(*snippet_admin_classes):
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
    form = SnippetForm
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs=text_area_attrs)}
    }
    # This was move here from model, otherwise first() and last() return the same when handling grouper queries
    ordering = ('name',)

    class Meta:
        model = Snippet

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return [
            url(
                r"^$",
                self.admin_site.admin_view(self.changelist_view),
                name="{}_{}_changelist".format(*info),
            ),
            url(
                r"^(?P<snippet_id>\d+)/$",
                self.admin_site.admin_view(self.changelist_view),
                name="{}_{}_list".format(*info),
            ),
            url(
                r"^add/$",
                self.admin_site.admin_view(self.add_view),
                name="{}_{}_add".format(*info),
            ),
            url(
                r"^(?P<object_id>\d+)/change/$",
                self.admin_site.admin_view(self.change_view),
                name="{}_{}_change".format(*info),
            ),
            url(
                r"^(?P<snippet_id>\d+)/preview/$",
                self.admin_site.admin_view(SnippetPreviewView.as_view()),
                name="{}_{}_preview".format(*info),
            ),
        ]


admin.site.register(Snippet, SnippetAdmin)
