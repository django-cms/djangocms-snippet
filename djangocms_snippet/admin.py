from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.urls import reverse

from cms.utils.permissions import get_model_permission_codename

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
                r"^(?P<snippet_id>\d+)/preview/$",
                self.admin_site.admin_view(SnippetPreviewView.as_view()),
                name="{}_{}_preview".format(*info),
            ),
        ] + super().get_urls()

    def has_delete_permission(self, request, obj=None):
        """
        When versioning is enabled, delete option is not available.
        If versioning is disabled, it may be possible to delete, as long as a user also has add permissions, and they
        are not in use.
        """
        if obj and not djangocms_versioning_enabled:
            return request.user.has_perm(
                get_model_permission_codename(self.model, 'add'),
            )
        return False

    def has_change_permission(self, request, obj=None):
        """
        Return edit mode if current user is the author, otherwise display snippet in read only mode
        """
        if obj and djangocms_versioning_enabled:
            created_by_id = self.get_version(obj).created_by_id
            logged_in_id = request.user.id
            version_state = self.get_version(obj).state
            if logged_in_id == created_by_id and version_state != 'published':
                return True
        return False

    def _get_preview_url(self, obj):
        """
        Return the change url which will be rendered in read only mode
        :return: method or None
        """
        change_url = reverse(
            "admin:{app}_{model}_change".format(
                app=obj._meta.app_label, model=self.model._meta.model_name
            ),
            args=(obj.pk,),
        )
        return change_url

    def get_list_actions(self):
        """
        Collect rendered actions from implemented methods and return as list
        """
        return [
            self._get_preview_link,
            self._get_edit_link,
            self._get_manage_versions_link,
        ]


admin.site.register(Snippet, SnippetAdmin)
