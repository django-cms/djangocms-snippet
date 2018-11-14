# -*- coding: utf-8 -*-
import sys

from django import template
from django.template.context import Context
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SnippetPtr


class SnippetPlugin(CMSPluginBase):
    model = SnippetPtr
    name = _('Snippet')
    render_template = 'djangocms_snippet/snippet.html'
    text_enabled = True
    text_editor_preview = False

    def render(self, context, instance, placeholder):
        context.update({
            'placeholder': placeholder,
            'object': instance,
        })
        try:
            if instance.snippet.template:
                t = template.loader.get_template(instance.snippet.template)
                context.update({
                    'html': mark_safe(instance.snippet.html)
                })
                content = t.render(Context(context))
            else:
                t = template.Template(instance.snippet.html)
                content = t.render(Context(context))
        except template.TemplateDoesNotExist:
            content = _('Template %(template)s does not exist.') % {
                'template': instance.snippet.template}
        except Exception:
            exc = sys.exc_info()[0]
            content = str(exc)
        context.update({
            'content': mark_safe(content),
        })
        return context


plugin_pool.register_plugin(SnippetPlugin)
