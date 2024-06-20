from importlib import reload
from unittest import skipIf

from cms import __version__ as cms_version
from cms.test_utils.testcases import CMSTestCase
from cms.utils import get_current_site
from django.contrib import admin
from django.contrib.sites.models import Site
from django.shortcuts import reverse
from django.test import RequestFactory, override_settings

try:
    from djangocms_versioning.models import Version
except ImportError:
    from tests.utils.models import Version

from djangocms_snippet import admin as snippet_admin
from djangocms_snippet.forms import SnippetForm
from djangocms_snippet.models import Snippet, SnippetGrouper


class SnippetAdminTestCase(CMSTestCase):
    def setUp(self):
        self.superuser = self.get_superuser()
        self.snippet = Snippet.objects.create(
            name="Test Snippet",
            slug="test-snippet",
            html="<h1>This is a test</h1>",
            snippet_grouper=SnippetGrouper.objects.create(),
        )
        self.snippet_version = Version.objects.create(
            content=self.snippet, created_by=self.superuser, state="published"
        )
        self.snippet_admin = snippet_admin.SnippetAdmin(Snippet, admin)
        self.snippet_admin_request = RequestFactory().get("/admin/djangocms_snippet")
        self.edit_url = reverse(
            "admin:djangocms_snippet_snippet_change",
            args=(self.snippet.id,),
        )
        self.delete_url = reverse(
            "admin:djangocms_snippet_snippet_delete",
            args=(self.snippet.id,),
        )

    def test_get_queryset(self):
        current_site = get_current_site()
        another_site = Site.objects.create(domain="http://www.django-cms.org", name="Django CMS", pk=3)
        current_site_snippet = Snippet.objects.create(
            name="Test Snippet 1",
            slug="test-snippet-one",
            html="<h1>This is a test snippet one</h1>",
            snippet_grouper=SnippetGrouper.objects.create(),
            site=current_site,
        )
        another_site_snippet = Snippet.objects.create(
            name="Test Snippet 2",
            slug="test-snippet-two",
            html="<h1>This is a test snippet two</h1>",
            snippet_grouper=SnippetGrouper.objects.create(),
            site=another_site,
        )
        # Create versions of snippets
        Version.objects.create(content=current_site_snippet, created_by=self.superuser, state="published")
        Version.objects.create(content=another_site_snippet, created_by=self.superuser, state="published")
        queryset = self.snippet_admin.get_queryset(self.snippet_admin_request)
        # Test for snippet of current site
        self.assertIn(current_site_snippet, queryset)
        # Test for snippet with no site
        self.assertIn(self.snippet, queryset)
        # Test for snippet with another site
        self.assertNotIn(another_site_snippet, queryset)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_admin_list_display_without_versioning(self):
        """
        Without versioning enabled, list_display should not be extended with version related items
        """
        admin.site.unregister(Snippet)
        reload(snippet_admin)
        # This has to be declared again, since it will now be constructed without the versioning extension
        self.snippet_admin = snippet_admin.SnippetAdmin(Snippet, admin)

        list_display = self.snippet_admin.get_list_display(self.snippet_admin_request)

        self.assertEqual(self.snippet_admin.__class__.__bases__, (admin.ModelAdmin,))
        self.assertEqual(list_display, ("slug", "name"))

    @skipIf(not cms_version.startswith("4.0."), "Django CMS 4 required")
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_list_display_with_versioning(self):
        """
        With versioning enabled, list_display should be populated with both versioning related items, and the
        list actions items
        """
        from djangocms_versioning.admin import ExtendedVersionAdminMixin

        list_display = self.snippet_admin.get_list_display(self.snippet_admin_request)

        # Mixins should always come first in the class bases
        self.assertEqual(self.snippet_admin.__class__.__bases__, (ExtendedVersionAdminMixin, admin.ModelAdmin))
        self.assertEqual(list_display[:-1], ("name", "get_author", "get_modified_date", "get_versioning_state"))
        self.assertEqual(list_display[-1].short_description.lower(), "actions")

    def test_admin_uses_form(self):
        """
        The SnippetForm provides functionality to make SnippetGroupers irrelevant to the user,
        ensure the admin uses this.
        """
        self.assertEqual(self.snippet_admin.form, SnippetForm)

    @skipIf(cms_version < "4", "Django CMS 4 required")
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_delete_button_disabled_versioning_enabled(self):
        """
        If versioning is enabled, the delete button should not be rendered on the change form
        """
        admin.site.unregister(Snippet)
        reload(snippet_admin)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.edit_url)

        self.assertNotContains(
            response, '<a href="/en/admin/djangocms_snippet/snippet/1/delete/" class="deletelink">Delete</a>'
        )

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_admin_delete_button_available_versioning_disabled(self):
        """
        If versioning is disabled, the delete button should be rendered on the change form
        """
        admin.site.unregister(Snippet)
        reload(snippet_admin)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.edit_url)

        self.assertContains(
            response, '<a href="/en/admin/djangocms_snippet/snippet/1/delete/" class="deletelink">Delete</a>'
        )

    @skipIf(cms_version < "4", "Django CMS 4 required")
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_delete_endpoint_inaccessible_versioning_enabled(self):
        """
        If versioning is enabled, the delete endpoint should not be accessible.
        """
        admin.site.unregister(Snippet)
        reload(snippet_admin)

        with self.login_user_context(self.superuser):
            response = self.client.post(self.delete_url)

        # The delete endpoint should return a 403 forbidden if we try to access it with versioning enabled
        self.assertEqual(response.status_code, 403)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_admin_delete_endpoint_accessible_versioning_disabled(self):
        """
        If versioning is disabled, the delete endpoint should be accessible.
        """
        admin.site.unregister(Snippet)
        reload(snippet_admin)

        with self.login_user_context(self.superuser):
            response = self.client.post(self.delete_url)

        # The delete endpoint should return a 200 success if we try to access it with versioning disabled
        self.assertEqual(response.status_code, 200)


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

    @skipIf(cms_version < "4", "Django CMS 4 required")
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_form_save_method(self):
        with self.login_user_context(self.superuser):
            response = self.client.post(
                self.add_url,
                {
                    "name": "Test Snippet 2",
                    "html": "<p>Test Save Snippet</p>",
                    "slug": "test-snippet-2",
                },
            )
            self.assertRedirects(response, self.changelist_url)

        # We should have 2 groupers and snippets, due to the creation of the others in setUp
        self.assertEqual(Snippet._base_manager.count(), 2)
        self.assertEqual(SnippetGrouper._base_manager.count(), 2)

    @skipIf(cms_version < "4", "Django CMS 4 required")
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_admin_form_edit_when_locked(self):
        """
        When a form is initialised in read-only mode, it should not require self.fields to be populated, and
        should return a read-only form.
        """
        self.snippet_version.publish(user=self.superuser)
        with self.login_user_context(self.superuser):
            edit_url = reverse(
                "admin:djangocms_snippet_snippet_change",
                args=(self.snippet.id,),
            )
            response = self.client.get(edit_url)

        # Check that we are loading in readonly mode
        self.assertContains(response, '<div class="readonly">Test Snippet</div>')
        # We should have the same number of snippets as before
        self.assertEqual(Snippet.objects.count(), 1)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_slug_colomn_should_hyperlinked_with_versioning_disabled(self):
        """
        Slug column should be visible and hyperlinked when versioning is disabled
        """
        admin.site.unregister(Snippet)
        reload(snippet_admin)

        with self.login_user_context(self.get_superuser()):
            response = self.client.get(self.changelist_url)
        self.assertContains(
            response,
            '<th class="field-slug"><a href="/en/admin/djangocms_snippet/' 'snippet/1/change/">test-snippet</a></th>',
        )

    @skipIf(cms_version < "4", "Django CMS 4 required")
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_name_colomn_should_not_be_hyperlinked_with_versioning_enabled(self):
        """
        Name column should be visible and not hyperlinked when versioning is enabled.
        Slug column should not be visible when versioning is enabled.
        """
        admin.site.unregister(Snippet)
        reload(snippet_admin)

        with self.login_user_context(self.get_superuser()):
            response = self.client.get(self.changelist_url)
        self.assertContains(response, '<td class="field-name">Test Snippet</td>')
        self.assertNotContains(
            response,
            '<th class="field-slug"><a href="/en/admin/djangocms_snippet/' 'snippet/1/change/">test-snippet</a></th>',
        )

    def test_preview_renders_read_only_fields(self):
        """
        Check that the preview endpoint is rendered in read only mode
        """
        self.snippet_version.publish(user=self.superuser)
        with self.login_user_context(self.superuser):
            edit_url = reverse(
                "admin:djangocms_snippet_snippet_preview",
                args=(self.snippet.id,),
            )
            response = self.client.get(edit_url)

        # Snippet name
        self.assertContains(response, '<div class="readonly">Test Snippet</div>')
        # Snippet slug
        self.assertContains(response, '<div class="readonly">test-snippet</div>')
        # Snippet HTML
        self.assertContains(response, '<div class="readonly">&lt;h1&gt;This is a test&lt;/h1&gt;</div>')
        # Snippet template
        self.assertContains(response, '<div class="readonly"></div>')
