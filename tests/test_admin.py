from importlib import reload

from django.contrib import admin
from django.shortcuts import reverse
from django.test import RequestFactory, override_settings

from cms.test_utils.testcases import CMSTestCase

from djangocms_versioning.models import Version

from djangocms_snippet import admin as snippet_admin
from djangocms_snippet import cms_config
from djangocms_snippet.forms import SnippetForm
from djangocms_snippet.models import Snippet, SnippetGrouper


class SnippetAdminTestCase(CMSTestCase):
    def setUp(self):
        self.snippet = Snippet.objects.create(
            name="Test Snippet",
            slug="test-snippet",
            html="<h1>This is a test</h1>",
            snippet_grouper=SnippetGrouper.objects.create(),
        )
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
        # This has to be declared again, since it will now be constructed without the versioning extension
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

    def test_admin_uses_form(self):
        """
        The SnippetForm provides functionality to make SnippetGroupers irrelevant to the user,
        ensure the admin uses this.
        """
        self.assertEqual(self.snippet_admin.form, SnippetForm)


class SnippetAdminFormTestCase(CMSTestCase):
    def setUp(self):
        self.add_url = reverse("admin:djangocms_snippet_snippet_add")
        self.changelist_url = reverse("admin:djangocms_snippet_snippet_changelist")
        self.superuser = self.get_superuser()
        self.snippet_grouper = SnippetGrouper.objects.create()
        self.snippet = Snippet.objects.create(
            name="Test Snippet",
            slug="test-snippet",
            html="<h1>This is a test</h1>",
            snippet_grouper=self.snippet_grouper,
        )
        self.snippet_version = Version.objects.create(content=self.snippet, created_by=self.superuser)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_form_save_method(self):
        with self.login_user_context(self.superuser):
            response = self.client.post(
                self.add_url,
                {
                    "name": "Test Snippet 2",
                    "html": "<p>Test Save Snippet</p>",
                    "slug": "test-snippet-2",
                })
            self.assertRedirects(response, self.changelist_url)

        # We should have 2 groupers and snippets, due to the creation of the others in setUp
        self.assertEqual(Snippet._base_manager.count(), 2)
        self.assertEqual(SnippetGrouper._base_manager.count(), 2)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_form_edit_when_locked(self):
        """
        When a form is initialised in read-only mode, it should not require self.fields to be populated, and
        should return a read-only form.
        """
        self.snippet_version.publish(user=self.superuser)
        with self.login_user_context(self.superuser):
            edit_url = reverse("admin:djangocms_snippet_snippet_change", args=(self.snippet.id,),)
            response = self.client.get(edit_url)

        # Check that we are loading in readonly mode
        self.assertContains(response, '<div class="readonly">Test Snippet</div>')
        # We should have the same number of snippets as before
        self.assertEqual(Snippet.objects.count(), 1)
