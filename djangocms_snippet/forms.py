from django import forms
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from djangocms_snippet.cms_config import SnippetCMSAppConfig
from djangocms_snippet.models import Snippet, SnippetGrouper


try:
    from djangocms_versioning import __version__  # NOQA
    is_versioning_installed = True
except ImportError:
    is_versioning_installed = False

djangocms_versioning_enabled = SnippetCMSAppConfig.djangocms_versioning_enabled


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = (
            "name",
            "html",
            "slug",
            "snippet_grouper",
            "template",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["snippet_grouper"].required = False
        self.fields["snippet_grouper"].widget = forms.HiddenInput()

    def clean(self):
        data = super().clean()
        name = data.get("name")
        slug = data.get("slug")
        snippet_grouper = data.get("snippet_grouper")
        snippet_queryset = Snippet.objects.all()

        if djangocms_versioning_enabled and is_versioning_installed:
            if snippet_grouper:
                snippet_queryset = snippet_queryset.exclude(snippet_grouper=snippet_grouper)

        for snippet in snippet_queryset:
            if snippet.name == name:
                self.add_error(
                    "name", _("A Snippet with this name already exists")
                )
            elif snippet.slug == slug:
                self.add_error(
                    "slug", _("A Snippet with this slug already exists")
                )

        return data

    @transaction.atomic
    def save(self, **kwargs):
        commit = kwargs.get("commit", True)
        snippet = super().save(commit=False)
        if commit:
            if not hasattr(snippet, "snippet_grouper"):
                snippet.snippet_grouper = SnippetGrouper.objects.create()
            snippet.save()
        return snippet
