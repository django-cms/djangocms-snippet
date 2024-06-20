from typing import ClassVar

from cms.models import CMSPlugin
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

# Search is enabled by default to keep backwards compatibility.
SEARCH_ENABLED = getattr(settings, "DJANGOCMS_SNIPPET_SEARCH", False)


class AdminQuerySet(models.QuerySet):
    def current_content(self, **kwargs):
        """If a versioning package is installed, this returns the currently valid content
        that matches the filter given in kwargs. Used to find content to be copied, e.g..
        Without versioning every page is current."""
        return self.filter(**kwargs)

    def latest_content(self, **kwargs):
        """If a versioning package is installed, returns the latest version that matches the
        filter given in kwargs including discarded or unpublished page content. Without versioning
        every page content is the latest."""
        return self.filter(**kwargs)


class SnippetGrouper(models.Model):
    """
    The Grouper model for snippet, this is required for versioning
    """

    def __str__(self):
        return self.name

    @property
    def name(self):
        snippet_qs = Snippet.admin_manager.filter(snippet_grouper=self)
        return snippet_qs.first().name or super().__str__

    def snippet(self, show_editable=False):  # NOQA: FBT002
        if show_editable:
            # When in "edit" or "preview" mode we should be able to see the latest content
            return (
                Snippet.admin_manager.current_content()
                .filter(
                    snippet_grouper=self,
                )
                .order_by("-pk")
                .first()
            )
        # When in "live" mode we should only be able to see the default published version
        return Snippet.objects.filter(snippet_grouper=self).first()


# Stores the actual data
class Snippet(models.Model):
    """
    A snippet of HTML or a Django template
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )
    snippet_grouper = models.ForeignKey(
        SnippetGrouper,
        on_delete=models.PROTECT,
    )
    html = models.TextField(
        verbose_name=_("HTML"),
        blank=True,
    )
    template = models.CharField(
        verbose_name=_("Template"),
        blank=True,
        max_length=255,
        help_text=_(
            'Enter a template (e.g. "snippets/plugin_xy.html") to '
            'be rendered. If "template" is given, the contents of '
            'field "HTML" will be passed as template variable '
            "{{ html }} to the template. Otherwise, the content of "
            '"HTML" is rendered.'
        ),
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        blank=False,
        default="",
        max_length=255,
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()
    admin_manager = AdminQuerySet.as_manager()

    class Meta:
        ordering: ClassVar[list[str]] = ["name"]
        verbose_name = _("Snippet")
        verbose_name_plural = _("Snippets")

    def __str__(self):
        return self.name

    def get_preview_url(self):
        return reverse(
            f"admin:{self._meta.app_label}_{self._meta.model_name}_preview",
            args=[self.id],
        )


# Plugin model - just a pointer to Snippet
class SnippetPtr(CMSPlugin):
    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name="%(app_label)s_%(class)s",
        parent_link=True,
        on_delete=models.CASCADE,
    )
    snippet_grouper = models.ForeignKey(
        SnippetGrouper,
        on_delete=models.CASCADE,
    )

    search_fields = ["snippet__html"] if SEARCH_ENABLED else []

    def get_short_description(self):
        snippet_label = SnippetGrouper.objects.filter(pk=self.snippet_grouper.pk).first()
        return snippet_label

    class Meta:
        verbose_name = _("Snippet Ptr")
        verbose_name_plural = _("Snippet Ptrs")

    def __str__(self):
        # Return the referenced snippet's name rather than the default (ID #)
        return self.snippet_grouper.name
