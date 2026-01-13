from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet.models import (
    SEARCH_ENABLED,
    Snippet,
    SnippetGrouper,
    SnippetPtr,
)

from .utils.factories import SnippetPluginFactory, SnippetWithVersionFactory


class SnippetModelTestCase(CMSTestCase):
    def setUp(self):
        self.snippet = SnippetWithVersionFactory(
            name="test snippet",
            html="<p>hello world</p>",
            slug="test_snippet",
        )
        self.snippet.versions.last().publish(user=self.get_superuser())
        self.snippet_grouper = self.snippet.snippet_grouper
        SnippetPluginFactory(snippet_grouper=self.snippet_grouper, language=["en"])

    def test_snippet_grouper_stays_when_snippet_deleted(self):
        """
        Test that the snippet grouper stays when a snippet is deleted.
        This is to ensure that the grouper is not deleted when there are
        other snippets associated with it.
        """
        temp_snippet = Snippet.objects.create(
            name="Temporary Snippet",
            snippet_grouper=self.snippet_grouper,
            html="<p>temporary</p>",
            slug="temporary_snippet",
        )
        self.assertTrue(Snippet.admin_manager.filter(pk=self.snippet.pk).exists())
        self.assertTrue(SnippetGrouper.objects.filter(pk=self.snippet_grouper.pk).exists())
        temp_snippet.delete()
        self.assertTrue(SnippetGrouper.objects.filter(pk=self.snippet_grouper.pk).exists())

    def test_snippet_grouper_deleted_with_last_snippet(self):
        grouper = SnippetGrouper.objects.create()
        snippet = Snippet.objects.create(
            name="Test Snippet",
            snippet_grouper=grouper,
            html="<p>test</p>",
            slug="test-snippet-2",
            site=self.snippet.site,
        )
        self.assertTrue(Snippet.admin_manager.filter(pk=snippet.pk).exists())
        self.assertTrue(SnippetGrouper.objects.filter(pk=grouper.pk).exists())
        snippet.delete()
        self.assertFalse(SnippetGrouper.objects.filter(pk=grouper.pk).exists())

    def test_settings(self):
        self.assertEqual(SEARCH_ENABLED, False)

    def test_snippet_instance(self):
        instance = Snippet.objects.all()

        self.assertEqual(instance.count(), 1)

        instance = Snippet.objects.first()

        self.assertEqual(instance.name, "test snippet")
        self.assertEqual(instance.html, "<p>hello world</p>")
        self.assertEqual(instance.slug, "test_snippet")
        # test strings
        self.assertEqual(str(instance), "test snippet")

    def test_snippet_ptr_instance(self):
        instance = SnippetPtr.objects.all()

        self.assertEqual(instance.count(), 1)

        instance = SnippetPtr.objects.first()

        # test strings
        self.assertEqual(instance.snippet_grouper.name, "test snippet")
