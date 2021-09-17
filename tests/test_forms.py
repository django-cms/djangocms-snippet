from django.test import override_settings

from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet.forms import SnippetForm
from djangocms_snippet.models import Snippet, SnippetGrouper


class SnippetFormTestCase(CMSTestCase):

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=False)
    def test_snippet_form_creates_grouper_no_versioning(self):
        """
        Without versioning enabled, the application still has the grouper implemented, therefore the form
        should be creating one for each new snippet created.
        """
        form_data = {
            "name": "test_snippet",
            "slug": "test_snippet",
            "html": "<h1>Test Title</h1>"
        }
        form = SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save()

        self.assertEqual(SnippetGrouper.objects.count(), 1)

    def test_snippet_form_creates_grouper_with_versioning(self):
        """
        With versioning enabled, groupers should also be created in the background.
        """
        form_data = {
            "name": "test_snippet",
            "slug": "test_snippet",
            "html": "<h1>Test Title</h1>"
        }
        form = SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save()

        self.assertEqual(SnippetGrouper.objects.count(), 1)

    def test_snippet_form_adds_to_existing_grouper_with_versioning(self):
        """
        With versioning enabled, if a grouper already exists, a new one shouldn't be created
        """

        grouper = SnippetGrouper.objects.create()
        form_data = {
            "name": "test_snippet",
            "slug": "test_snippet",
            "html": "<h1>Test Title</h1>",
            "snippet_grouper": grouper.id,
        }
        form = SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save()

        self.assertEqual(SnippetGrouper.objects.count(), 1)

        form_data["html"] = "<h2>Test Title</h2>"

        form = SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        form.clean()
        form.save()

        self.assertEqual(SnippetGrouper.objects.count(), 1)

    def test_snippet_form_versioning_enabled(self):
        """
        With versioning enabled, the snippet form doesn't have to create groupers, but does have to validate
        that no other active (i.e. the latest published snippet from a given grouper) shares the same name or slug.
        """
        form_data = {
            "name": "test_snippet",
            "slug": "test_snippet",
            "html": "<h1>Test Title</h1>",
        }
        form = SnippetForm(form_data)

        self.assertTrue(form.is_valid())

        # Clean and save the form
        form.clean()
        form.save()

        snippet = Snippet._base_manager.last()
        version = snippet.versions.create(created_by=self.get_superuser())
        version.publish(user=self.get_superuser())

        new_form_data = {
            "name": "test_snippet1",
            "slug": "test_snippet",
            "html": "<h1>Another Test Title</h1>",
        }

        new_form = SnippetForm(new_form_data)

        self.assertFalse(new_form.is_valid())

        new_form.clean()

        self.assertDictEqual(new_form.errors, {'slug': ['Snippet with this slug already exists']})
