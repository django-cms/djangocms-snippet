# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SnippetPtr


CACHE_ENABLED = getattr(settings, "DJANGOCMS_SNIPPET_CACHE", False)


class SnippetPlugin(CMSPluginBase):
    model = SnippetPtr
    name = _("Snippet")
    render_template = "djangocms_snippet/snippet.html"
    text_enabled = True
    text_editor_preview = False
    cache = CACHE_ENABLED

    def render(self, context, instance, placeholder):
        try:
            if instance.snippet.template:
                context = context.flatten()
                context.update({"html": mark_safe(instance.snippet.html)})
                t = template.loader.get_template(instance.snippet.template)
                content = t.render(context)
            else:
                # only html provided
                t = template.Template(instance.snippet.html)
                content = t.render(context)
        except template.TemplateDoesNotExist:
            content = _("Template %(template)s does not exist.") % {
                "template": instance.snippet.template
            }
        except Exception as e:
            content = escape(str(e))

        context.update(
            {
                "placeholder": placeholder,
                "object": instance,
                "html": mark_safe(instance.snippet.html),
                "content": content,
            }
        )

        return context


plugin_pool.register_plugin(SnippetPlugin)
