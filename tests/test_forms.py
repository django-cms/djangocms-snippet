from importlib import reload
from unittest import skipIf

from cms import __version__ as cms_version
from cms.test_utils.testcases import CMSTestCase
from django.test import override_settings

from djangocms_snippet import forms
from djangocms_snippet.forms import SnippetPluginForm
from djangocms_snippet.models import Snippet, SnippetGrouper

from .utils.factories import SnippetWithVersionFactory


class SnippetFormTestCase(CMSTestCase):
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_snippet_form_creates_grouper_no_versioning(self):
        """
        Without versioning enabled, the application still has the grouper implemented, therefore the form
        should be creating one for each new snippet created.
        """
        reload(forms)
        form_data = {"name": "test_snippet", "slug": "test_snippet", "html": "<h1>Test Title</h1>"}
        form = forms.SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save(commit=True)

        self.assertEqual(SnippetGrouper.objects.count(), 1)
        self.assertEqual(Snippet._base_manager.count(), 1)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_snippet_form_creates_grouper_with_versioning(self):
        """
        With versioning enabled, groupers should also be created in the background.
        """
        reload(forms)
        form_data = {"name": "test_snippet", "slug": "test_snippet", "html": "<h1>Test Title</h1>"}
        form = forms.SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save(commit=True)

        self.assertEqual(SnippetGrouper.objects.count(), 1)
        self.assertEqual(Snippet._base_manager.count(), 1)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_snippet_form_doesnt_create_grouper_or_snippet_with_no_commit(self):
        """
        With versioning enabled, but no commit flag, models should still be created
        """
        reload(forms)
        form_data = {"name": "test_snippet", "slug": "test_snippet", "html": "<h1>Test Title</h1>"}
        form = forms.SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save()

        self.assertEqual(SnippetGrouper.objects.count(), 1)
        self.assertEqual(Snippet._base_manager.count(), 1)

    @skipIf(cms_version < "4", "Django CMS 4 required")
    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_snippet_form_adds_to_existing_grouper_with_versioning(self):
        """
        With versioning enabled, if a grouper already exists, a new one shouldn't be created
        """
        reload(forms)
        grouper = SnippetGrouper.objects.create()
        form_data = {
            "name": "test_snippet",
            "slug": "test_snippet",
            "html": "<h1>Test Title</h1>",
            "snippet_grouper": grouper.id,
        }
        form = forms.SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save(commit=True)

        self.assertEqual(SnippetGrouper.objects.count(), 1)
        self.assertEqual(Snippet._base_manager.count(), 1)

        form_data["html"] = "<h2>Test Title</h2>"

        form = forms.SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save(commit=True)

        self.assertEqual(SnippetGrouper.objects.count(), 1)
        self.assertEqual(Snippet._base_manager.count(), 2)

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_snippet_form_versioning_enabled(self):
        """
        With versioning enabled, the snippet form doesn't have to create groupers, but does have to validate
        that no other active (i.e. the latest published snippet from a given grouper) shares the same name or slug.
        """
        reload(forms)
        form_data = {
            "name": "test_snippet",
            "slug": "test_snippet",
            "html": "<h1>Test Title</h1>",
        }
        form = forms.SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        # Clean and save the form
        form.clean()
        snippet = form.save(commit=True)

        version = snippet.versions.create(created_by=self.get_superuser())
        version.publish(user=self.get_superuser())

        new_form_data = {
            "name": "test_snippet1",
            "slug": "test_snippet",
            "html": "<h1>Another Test Title</h1>",
        }

        new_form = forms.SnippetForm(new_form_data)

        self.assertFalse(new_form.is_valid())

        new_form.clean()

        self.assertDictEqual(new_form.errors, {"slug": ["A Snippet with this slug already exists"]})

    @skipIf(cms_version < "4", "Django CMS 4 required")
    def test_snippet_form_validation_multiple_version_states_in_grouper(self):
        """
        Snippet forms should be valid regardless of the versions, or states which already exist within its grouper.
        """
        reload(forms)
        # snippet_to_archive starts as draft
        snippet_to_archive = SnippetWithVersionFactory()
        # Then it is published it
        snippet_to_archive.versions.first().publish(user=self.get_superuser())
        # snippet_to_publish starts as a draft
        snippet_to_publish = SnippetWithVersionFactory(
            name=snippet_to_archive.name,
            slug=snippet_to_archive.slug,
            snippet_grouper=snippet_to_archive.snippet_grouper,
        )
        # Snippet_to_publish is published, archiving snippet_to_archive
        snippet_to_publish.versions.first().publish(user=self.get_superuser())
        # Create a new draft in the same grouper
        SnippetWithVersionFactory(
            name=snippet_to_archive.name,
            slug=snippet_to_archive.slug,
            snippet_grouper=snippet_to_archive.snippet_grouper,
        )

        form_data = {
            "name": snippet_to_archive.name,
            "slug": snippet_to_archive.slug,
            "html": "<p>Hello World!</p>",
            "snippet_grouper": snippet_to_archive.snippet_grouper.id,
        }

        form = forms.SnippetForm(form_data)

        self.assertTrue(form.is_valid())


class SnippetPluginFormTestCase(CMSTestCase):
    def setUp(self):
        self.form = SnippetPluginForm()

    def test_get_related_url_for_snippet(self):
        """
        Check that the url to add a snippet in the admin is returned
        """
        self.assertEqual(self.form.get_related_url_for_snippet("", "add"), "/en/admin/djangocms_snippet/snippet/add/")

    def test_get_related_url_for_snippet_used(self):
        """
        Checks that the get_related_url widget is overridden
        """
        snippet_grouper_widget = self.form.fields["snippet_grouper"].widget
        self.assertEqual(snippet_grouper_widget.get_related_url, self.form.get_related_url_for_snippet)
        self.assertTrue(snippet_grouper_widget.can_add_related)
