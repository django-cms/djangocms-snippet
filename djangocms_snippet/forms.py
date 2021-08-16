from django import forms

from djangocms_snippet.models import Snippet, SnippetGrouper
from djangocms_snippet.utils import is_versioning_enabled


class SnippetForm(forms.ModelForm):
    class Meta:
        fields = ["name", "html", "template", "slug"]
        model = Snippet

    def clean(self):
        cleaned_data = super().clean()
        if is_versioning_enabled and not cleaned_data.get("snippet_grouper"):
            cleaned_data["snippet_grouper"] = SnippetGrouper.objects.create()
        return cleaned_data
