# -*- coding: utf-8 -*-
"""
Snippet template tags
"""
import six
from contextlib import contextmanager

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from djangocms_snippet.models import Snippet

register = template.Library()


@contextmanager
def exceptionless(truth):
    # Accepts one truth parameter, when 'False' normal behavior
    # when 'True' any expection will be suppressed
    try:
        yield
    except Exception:
        if truth:
            # WARNING: suppressing exception
            pass
        else:
            # Reraising exception
            raise


class SnippetFragment(template.Node):
    """
    Get a snippet HTML fragment
    """

    def __init__(self, snippet_id_varname, *args):
        """
        :type insert_instance_varname: string or object
                                       ``django.db.models.Model``
        :param insert_instance_varname: Instance variable name or a string slug
                                        or object id
        """
        self.parse_until = False
        self.snippet_id_varname = template.Variable(snippet_id_varname)
        if args and 'or' in args:
            # We are in a 'parse util' case
            # ALERT: Exceptions will be suppressed to avoid errors from bad
            # tag content
            # Maybe we could analyze more usage case to catch only exceptions
            # related to bad tag content
            self.parse_until = True
            self.nodelist = args[1]

    def render(self, context):
        """
        :type context: object ``django.template.Context``
        :param context: Context tag object

        :rtype: string
        :return: the HTML for the snippet
        """
        # Default assume this is directly an instance
        snippet_instance = self.snippet_id_varname.resolve(context)
        # Assume this is slug
        with exceptionless(self.parse_until):
            if isinstance(snippet_instance, six.string_types):
                snippet_instance = Snippet.objects.get(slug=snippet_instance)
            # Assume this is an id
            elif isinstance(snippet_instance, int):
                snippet_instance = Snippet.objects.get(pk=snippet_instance)

            return mark_safe(self.get_content_render(context,
                                                     snippet_instance))

        # Rely on the fact that manager something went wrong
        # render the fallback template
        return self.nodelist.render(context)

    def get_content_render(self, context, instance):
        """
        Render the snippet HTML, using a template if defined in its instance
        """
        context.update({
            'object': instance,
        })
        try:
            if instance.template:
                t = template.loader.get_template(instance.template)
                context.update({
                    'html': mark_safe(instance.html)
                })
                content = t.render(template.Context(context))
            else:
                t = template.Template(instance.html)
                content = t.render(template.Context(context))
        except template.TemplateDoesNotExist:
            content = _('Template %(template)s does not exist.') % {
                'template': instance.template}
        except Exception as e:
            content = str(e)
            if self.parse_until:
                # In case we are running 'exceptionless'
                # Re-raise exception in order not to get the
                # error rendered
                raise
        return content


@register.tag(name='snippet_fragment')
def do_snippet_fragment(parser, token):
    """
    Display a snippet HTML fragment

    Usage : ::
        {% snippet_fragment [Snippet ID or instance] %}

        {% snippet_fragment [Snippet ID or instance] or %}
            ...This is a fallback...
        {% endsnippet_fragment %}
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            'You need to specify at least a "snippet" ID, slug or instance')
    if 'or' in args:
        # Catch contents between tags and pass to renderer
        args.append(parser.parse(('endsnippet_fragment',)))
        parser.delete_first_token()
    return SnippetFragment(*args[1:])


do_snippet_fragment.is_safe = True
