from django.views.generic import TemplateView


class SnippetPreviewView(TemplateView):
    template_name = "djangocms_snippet/admin/preview.html"
