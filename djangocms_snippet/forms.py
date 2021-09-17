from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from djangocms_snippet.models import Snippet, SnippetGrouper


try:
    from djangocms_versioning.models import Version
    is_versioning_installed = True
except ImportError:
    is_versioning_installed = False

djangocms_versioning_enabled = getattr(
        settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED', False
    )


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = (
            "name",
            "html",
            "slug",
            "snippet_grouper",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["snippet_grouper"].required = False

    def clean(self):
        data = super().clean()
        name = data.get("name")
        slug = data.get("slug")
        snippet_grouper = data.get("snippet_grouper")
        published_snippet_queryset = Snippet.objects.all()

        if djangocms_versioning_enabled and is_versioning_installed:
            if snippet_grouper:
                published_snippet_queryset.exclude(snippet_grouper=snippet_grouper)

        for snippet in published_snippet_queryset:
            if snippet.name == name:
                self.add_error(
                    "name", _("Snippet with this name already exists")
                )
            elif snippet.slug == slug:
                self.add_error(
                    "slug", _("Snippet with this slug already exists")
                )

        return data

    def save(self, **kwargs):
        if not self.cleaned_data.get("snippet_grouper"):
            super().save(commit=False)
            self.instance.snippet_grouper = SnippetGrouper.objects.create()
            # self.instance.snippet_grouper_id = self.snippet_grouper.id
        return super().save()


