from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet.models import SEARCH_ENABLED, Snippet, SnippetPtr

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
        self.assertEqual(str(instance), "test snippet")
