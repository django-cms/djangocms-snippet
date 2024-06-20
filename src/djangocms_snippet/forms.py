from cms.utils.urlutils import admin_reverse
from django import forms
from django.contrib import admin
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from djangocms_snippet.models import Snippet, SnippetGrouper, SnippetPtr
from djangocms_snippet.utils import (
    djangocms_versioning_enabled,
    is_versioning_installed,
)


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = (
            "name",
            "html",
            "slug",
            "snippet_grouper",
            "template",
            "site",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("snippet_grouper"):
            self.fields["snippet_grouper"].required = False
            self.fields["snippet_grouper"].widget = forms.HiddenInput()

    def clean(self):
        data = super().clean()
        name = data.get("name")
        slug = data.get("slug")
        snippet_grouper = data.get("snippet_grouper")
        snippet_queryset = Snippet.objects.all()

        if djangocms_versioning_enabled and is_versioning_installed and snippet_grouper:
            snippet_queryset = snippet_queryset.exclude(snippet_grouper=snippet_grouper)

        for snippet in snippet_queryset:
            if snippet.name == name:
                self.add_error("name", _("A Snippet with this name already exists"))
            elif snippet.slug == slug:
                self.add_error("slug", _("A Snippet with this slug already exists"))

        return data

    @transaction.atomic
    def save(self, **kwargs):
        commit = kwargs.get("commit", True)
        snippet = super().save(commit=False)
        if not hasattr(snippet, "snippet_grouper"):
            snippet.snippet_grouper = SnippetGrouper.objects.create()
        if commit:
            snippet.save()
        return snippet


class SnippetPluginForm(forms.ModelForm):
    class Meta:
        model = SnippetPtr
        fields = ("cmsplugin_ptr", "snippet_grouper")

    def __init__(self, *args, **kwargs):
        """
        Initialise the form with the add button enabled to allow adding a new snippet from the plugin form. To enable
        this the get_related_url method on the widget is overridden to build a URL for the Snippet admin instead of
        the SnippetGrouper, as this is not enabled in the admin.
        """
        super().__init__(*args, **kwargs)
        self.fields["snippet_grouper"].widget.can_add_related = True
        self.fields["snippet_grouper"].widget.get_related_url = self.get_related_url_for_snippet

    def get_related_url_for_snippet(self, info, action, *args):
        """
        Build URL to the Snippet admin for the given action
        """
        return admin_reverse(f"djangocms_snippet_snippet_{action}", current_app=admin.site.name, args=args)
