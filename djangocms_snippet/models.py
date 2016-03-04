# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.utils.compat.dj import python_2_unicode_compatible
from cms.utils.helpers import reversion_register


# Search is enabled by default to keep backwards compatibility.
SEARCH_ENABLED = getattr(settings, 'DJANGOCMS_SNIPPET_SEARCH', False)


# Stores the actual data
@python_2_unicode_compatible
class Snippet(models.Model):
    """
    A snippet of HTML or a Django template
    """
    name = models.CharField(_("name"), max_length=255, unique=True)
    html = models.TextField(_("HTML"), blank=True)
    template = models.CharField(
        _("template"), max_length=50, blank=True,
        help_text=_('Enter a template (i.e. "snippets/plugin_xy.html") which '
                    'will be rendered. If "template" is given, the contents of '
                    'field "HTML" will be passed as template variable '
                    '{{ html }} to the template. Else, the content of "HTML" '
                    'is rendered.'))
    slug = models.SlugField(
        _('slug'), max_length=75, unique=True, blank=False, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("Snippet")
        verbose_name_plural = _("Snippets")


# Plugin model - just a pointer to Snippet
@python_2_unicode_compatible
class SnippetPtr(CMSPlugin):
    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='djangocms_snippet_snippetptr',
        parent_link=True)

    snippet = models.ForeignKey(Snippet)

    search_fields = ['snippet__html'] if SEARCH_ENABLED else []

    class Meta:
        verbose_name = _("Snippet")

    def __str__(self):
        # Return the referenced snippet's name rather than the default (ID #)
        return self.snippet.name


# We don't both with SnippetPtr, since all the data is actually in Snippet
reversion_register(Snippet)
