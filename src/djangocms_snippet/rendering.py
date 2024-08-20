from django.template.response import TemplateResponse


def render_snippet(request, snippet):
    template = "djangocms_snippet/admin/preview.html"
    context = {"snippet": snippet}
    return TemplateResponse(request, template, context)
