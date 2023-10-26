"""
Snippet template tags
"""
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from django import template
from django.template.base import Parser, Token
from django.template.context import BaseContext
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from djangocms_snippet.models import Snippet

register = template.Library()

EXPECTED_LENGTH = 2


@contextmanager
def exceptionless(truth: bool) -> Generator[None, None, None]:
    """
    Accepts one truth parameter, when 'False' normal behavior
    when 'True' any exception will be suppressed
    """
    try:
        yield
    except Exception:
        if truth:
            # WARNING: suppressing exception
            pass
        else:
            # Re-raising exception
            raise


class SnippetFragment(template.Node):
    """
    Get a snippet HTML fragment
    """

    def __init__(self, snippet_id_varname: str, *args: Any):
        """
        :type insert_instance_varname: string or object
                                       ``django.db.models.Model``
        :param insert_instance_varname: Instance variable name or a string slug
                                        or object id
        """
        self.parse_until = False
        self.snippet_id_varname = template.Variable(snippet_id_varname)
        if args and "or" in args:
            # We are in a 'parse util' case
            # ALERT: Exceptions will be suppressed to avoid errors from bad
            # tag content
            # Maybe we could analyze more usage case to catch only exceptions
            # related to bad tag content
            self.parse_until = True
            self.nodelist = args[1]

    def render(self, context: BaseContext) -> str:
        """
        :type context: dict
        :param context: Context tag object

        :rtype: string
        :return: the HTML for the snippet
        """
        # Default assume this is directly an instance
        snippet_instance = self.snippet_id_varname.resolve(context)

        response = self.nodelist.render(context)
        # Assume this is slug
        with exceptionless(self.parse_until):
            if isinstance(snippet_instance, str):
                snippet_instance = Snippet.objects.get(slug=snippet_instance)
            # Assume this is an id
            elif isinstance(snippet_instance, int):  # pragma: no cover
                snippet_instance = Snippet.objects.get(pk=snippet_instance)

            response = mark_safe(
                self.get_content_render(context, snippet_instance)
            )

        return response

    def get_content_render(
        self, context: BaseContext, instance: Snippet
    ) -> str:
        """
        Render the snippet HTML, using a template if defined in its instance
        """
        context.update(
            {
                "object": instance,
            }
        )
        try:
            if instance.template:
                context.update({"html": mark_safe(instance.html)})
                content = template.loader.render_to_string(
                    instance.template,
                    context.flatten(),
                )
            else:
                t = template.Template(instance.html)
                content = t.render(context)
        except template.TemplateDoesNotExist:
            content = _("Template %(template)s does not exist.") % {
                "template": instance.template
            }
        except Exception as e:  # pragma: no cover
            content = escape(str(e))
            if self.parse_until:
                # In case we are running 'exceptionless'
                # Re-raise exception in order not to get the
                # error rendered
                raise
        return content


@register.tag(name="snippet_fragment")
def do_snippet_fragment(parser: Parser, token: Token) -> SnippetFragment:
    """
    Display a snippet HTML fragment

    Usage : ::
        {% snippet_fragment [Snippet ID or instance] %}

        {% snippet_fragment [Snippet ID or instance] or %}
            ...This is a fallback...
        {% endsnippet_fragment %}
    """
    args = token.split_contents()
    if len(args) < EXPECTED_LENGTH:
        raise template.TemplateSyntaxError(
            'You need to specify at least a "snippet" ID, slug or instance'
        )
    if "or" in args:
        # Catch contents between tags and pass to renderer
        args.append(parser.parse(("endsnippet_fragment",)))
        parser.delete_first_token()
    return SnippetFragment(*args[1:])


do_snippet_fragment.is_safe = True
