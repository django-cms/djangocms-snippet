from typing import Any, ClassVar

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    class Media:
        js = (
            "admin/vendor/ace/ace.js"
            if "djangocms_static_ace" in settings.INSTALLED_APPS
            else "https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/ace.js",
        )

    list_display = ("slug", "name")
    search_fields: ClassVar[list[str]] = ["slug", "name"]
    prepopulated_fields: ClassVar[dict[str, tuple[str]]] = {"slug": ("name",)}
    change_form_template = "djangocms_snippet/admin/change_form.html"
    text_area_attrs: ClassVar[dict[str, Any]] = {
        "rows": 20,
        "data-editor": True,
        "data-mode": getattr(settings, "DJANGOCMS_SNIPPET_THEME", "html"),
        "data-theme": getattr(settings, "DJANGOCMS_SNIPPET_MODE", "github"),
    }

    formfield_overrides: ClassVar[dict[Any, dict[str, Any]]] = {
        models.TextField: {"widget": Textarea(attrs=text_area_attrs)}
    }
