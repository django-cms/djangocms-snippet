from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SnippetPtr
from .utils import show_draft_content


CACHE_ENABLED = getattr(settings, "DJANGOCMS_SNIPPET_CACHE", False)


class SnippetPlugin(CMSPluginBase):
    model = SnippetPtr
    name = _("Snippet")
    render_template = "djangocms_snippet/snippet.html"
    text_enabled = True
    text_editor_preview = False
    cache = CACHE_ENABLED

    def render(self, context, instance, placeholder):
        snippet = instance.snippet_grouper.snippet(show_editable=show_draft_content(context["request"]))
        try:
            if snippet.template:
                context = context.flatten()
                context.update({"html": mark_safe(snippet.html)})
                t = template.loader.get_template(snippet.template)
                content = t.render(context)
            else:
                # only html provided
                t = template.Template(snippet.html)
                content = t.render(context)
        except template.TemplateDoesNotExist:
            content = _("Template %(template)s does not exist.") % {
                "template": snippet.template
            }
        except Exception as e:
            content = escape(str(e))

        context.update(
            {
                "placeholder": placeholder,
                "object": instance,
                "html": mark_safe(snippet.html),
                "content": content,
            }
        )

        return context


plugin_pool.register_plugin(SnippetPlugin)
