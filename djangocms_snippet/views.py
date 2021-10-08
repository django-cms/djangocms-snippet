from django.http import Http404
from django.views.generic import TemplateView

from djangocms_snippet.models import Snippet


class SnippetPreviewView(TemplateView):
    template_name = "djangocms_snippet/admin/preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            snippet = Snippet._base_manager.get(pk=self.kwargs.get("snippet_id"))
        except Snippet.DoesNotExist:
            raise Http404

        context.update({
            "snippet": snippet,
            "opts": Snippet._meta
        })
        return context
