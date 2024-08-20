from typing import Any, ClassVar

from cms.utils import get_current_site
from cms.utils.permissions import get_model_permission_codename
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR
from django.contrib.admin.utils import flatten_fieldsets, unquote
from django.db import models
from django.forms import Textarea
from django.urls import path
from django.utils.translation import gettext as _

from .forms import SnippetForm
from .models import Snippet

# Use the version mixin if djangocms-versioning is installed and enabled
snippet_admin_classes = [admin.ModelAdmin]
djangocms_versioning_enabled = getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_ENABLED", True)

try:
    try:
        from djangocms_versioning.admin import (
            ExtendedIndicatorVersionAdminMixin,
        )
    except ImportError:
        from djangocms_versioning.admin import (
            ExtendedVersionAdminMixin as ExtendedIndicatorVersionAdminMixin,
        )

    if djangocms_versioning_enabled:
        snippet_admin_classes.insert(0, ExtendedIndicatorVersionAdminMixin)
except ImportError:
    djangocms_versioning_enabled = False


@admin.register(Snippet)
class SnippetAdmin(*snippet_admin_classes):
    class Media:
        js = (
            "admin/vendor/ace/ace.js"
            if "djangocms_static_ace" in settings.INSTALLED_APPS
            else "https://cdnjs.cloudflare.com/ajax/libs/ace/1.33.3/ace.js",
        )

    list_display = ("name",)
    search_fields: ClassVar[list[str]] = ["name"]
    change_form_template = "djangocms_snippet/admin/change_form.html"
    text_area_attrs: ClassVar[dict[str, Any]] = {
        "rows": 20,
        "data-editor": True,
        "data-mode": getattr(settings, "DJANGOCMS_SNIPPET_THEME", "html"),
        "data-theme": getattr(settings, "DJANGOCMS_SNIPPET_MODE", "github"),
    }
    form = SnippetForm
    formfield_overrides: ClassVar[dict] = {models.TextField: {"widget": Textarea(attrs=text_area_attrs)}}
    # This was move here from model, otherwise first() and last() return the same when handling grouper queries
    ordering = ("name",)

    class Meta:
        model = Snippet

    def get_queryset(self, request):
        site = get_current_site()
        queryset = super().get_queryset(request)
        # Filter queryset with current site and no site
        queryset = queryset.filter(models.Q(site=site) | models.Q(site=None))
        return queryset

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display = list(list_display)

        if not djangocms_versioning_enabled:
            list_display.insert(0, "slug")

        list_display = tuple(list_display)
        return list_display

    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        if not djangocms_versioning_enabled:
            search_fields.append("slug")
        return search_fields

    def get_prepopulated_fields(self, obj, request):
        prepopulated_fields = super().get_prepopulated_fields(request)
        if not djangocms_versioning_enabled:
            prepopulated_fields = {"slug": ("name",)}
        return prepopulated_fields

    def get_list_display_links(self, request, list_display):
        if not djangocms_versioning_enabled:
            return list(list_display)[:1]
        else:
            self.list_display_links = (None,)
            return self.list_display_links

    def preview_view(self, request, snippet_id=None, form_url="", extra_context=None):
        """
        Custom preview endpoint to display a change form in read only mode
        Solution based on django changeform view implementation
        https://github.com/django/django/blob/4b8e9492d9003ca357a4402f831112dd72efd2f8/django/contrib/admin/options.py#L1553
        """
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))

        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField(f"The field {to_field} cannot be referenced.")

        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(str(snippet_id)), to_field)

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, str(snippet_id))

        fieldsets = self.get_fieldsets(request, obj)
        model_form = self.get_form(request, obj, change=False, fields=flatten_fieldsets(fieldsets))
        form = model_form(instance=obj)
        formsets, inline_instances = self._create_formsets(request, obj, change=True)

        readonly_fields = flatten_fieldsets(fieldsets)

        admin_form = helpers.AdminForm(
            form,
            list(fieldsets),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            {},
            readonly_fields,
            model_admin=self,
        )
        media = self.media + admin_form.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        title = _("View %s")
        context = {
            **self.admin_site.each_context(request),
            "title": title % opts.verbose_name,
            "subtitle": str(obj) if obj else None,
            "adminform": admin_form,
            "object_id": snippet_id,
            "original": obj,
            "is_popup": IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            "to_field": to_field,
            "media": media,
            "inline_admin_formsets": inline_formsets,
            "errors": [],
            "preserved_filters": self.get_preserved_filters(request),
        }

        context.update(extra_context or {})

        return self.render_change_form(
            request,
            context,
            add=False,
            change=False,
            obj=obj,
            form_url=form_url,
        )

    def get_urls(self):
        return [
            path(
                "<int:snippet_id>/preview/",
                self.admin_site.admin_view(self.preview_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_preview",
            ),
            *super().get_urls(),
        ]

    def has_delete_permission(self, request, obj=None):
        """
        When versioning is enabled, delete option is not available.
        If versioning is disabled, it may be possible to delete, as long as a user also has add permissions, and they
        are not in use.
        """
        if obj and not djangocms_versioning_enabled:
            return request.user.has_perm(
                get_model_permission_codename(self.model, "add"),
            )
        return False
