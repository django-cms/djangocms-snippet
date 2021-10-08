from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from djangocms_snippet.models import Snippet


class SnippetPreviewView(TemplateView):
    template_name = "djangocms_snippet/admin/preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snippet_qs = Snippet._base_manager.filter(pk=self.kwargs.get("snippet_id"))
        snippet = snippet_qs[0]
        context.update({
            "snippet": snippet,
            "opts": Snippet._meta
        })
        return context
