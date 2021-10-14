from importlib import reload

from django.contrib import admin
from django.test import RequestFactory, override_settings

from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet import admin as snippet_admin
from djangocms_snippet import cms_config
from djangocms_snippet.models import Snippet

from .utils.factories import SnippetWithVersionFactory


class SnippetAdminTestCase(CMSTestCase):
    def setUp(self):
        self.snippet = SnippetWithVersionFactory()
        self.snippet_admin = snippet_admin.SnippetAdmin(Snippet, admin)
        self.snippet_admin_request = RequestFactory().get("/admin/djangocms_snippet")

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_admin_list_display_without_versioning(self):
        """
        Without versioning enabled, list_display should not be extended with version related items
        """
        admin.site.unregister(Snippet)
        reload(cms_config)
        reload(snippet_admin)
        self.snippet_admin = snippet_admin.SnippetAdmin(Snippet, admin)

        list_display = self.snippet_admin.get_list_display(self.snippet_admin_request)

        self.assertEqual(self.snippet_admin.__class__.__bases__, (admin.ModelAdmin, ))
        self.assertEqual(list_display, ('slug', 'name'))

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_list_display_with_versioning(self):
        """
        With versioning enabled, list_display should be populated with both versioning related items, and the
        list actions items
        """
        from djangocms_versioning.admin import ExtendedVersionAdminMixin
        list_display = self.snippet_admin.get_list_display(self.snippet_admin_request)

        # Mixins should always come first in the class bases
        self.assertEqual(
            self.snippet_admin.__class__.__bases__, (ExtendedVersionAdminMixin, admin.ModelAdmin)
        )
        self.assertEqual(
            list_display[:-1], ('slug', 'name', 'get_author', 'get_modified_date', 'get_versioning_state')
        )
        self.assertEqual(list_display[-1].short_description, 'actions')
        self.assertIn("function ExtendedVersionAdminMixin._list_actions", list_display[-1].__str__())
