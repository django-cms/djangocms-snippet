from importlib import reload

from django.contrib import admin
from django.test import override_settings, RequestFactory


from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet import admin as snippet_admin
from djangocms_snippet.models import Snippet

from .utils.factories import SnippetWithVersionFactory


class SnippetAdminTestCase(CMSTestCase):
    def setUp(self):
        self.snippet = SnippetWithVersionFactory()
        self.snippet_admin = snippet_admin.SnippetAdmin(Snippet, admin)
        self.snippet_admin_request = RequestFactory().get("/admin/djangocms_snippet")

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_admin_without_versioning(self):
        admin.site.unregister(Snippet)
        reload(snippet_admin)
        self.snippet_admin = snippet_admin.SnippetAdmin(Snippet, admin)

        list_display = self.snippet_admin.get_list_display(self.snippet_admin_request)

        self.assertEqual(self.snippet_admin.__class__.__bases__, (snippet_admin.AbstractSnippetAdmin,))
        self.assertEqual(list_display, ('slug', 'name'))

    def test_admin_with_versioning(self):
        from djangocms_versioning.admin import ExtendedVersionAdminMixin
        list_display = self.snippet_admin.get_list_display(self.snippet_admin_request)

        self.assertEqual(
            self.snippet_admin.__class__.__bases__, (ExtendedVersionAdminMixin, snippet_admin.AbstractSnippetAdmin)
        )
        self.assertEqual(
            list_display[:-1], ('slug', 'name', 'get_author', 'get_modified_date', 'get_versioning_state')
        )
        self.assertEqual(list_display[-1].short_description, 'actions')
