from django.test import TestCase

from djangocms_snippet.models import SEARCH_ENABLED, Snippet, SnippetPtr


class SnippetModelTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_settings(self):
        self.assertEqual(SEARCH_ENABLED, False)

    def test_snippet_instance(self):
        Snippet.objects.create(
            name="test snippet",
            html="<p>hello world</p>",
            slug="test_snippet",
        )
        instance = Snippet.objects.all()
        self.assertEqual(instance.count(), 1)
        instance = Snippet.objects.first()
        self.assertEqual(instance.name, "test snippet")
        self.assertEqual(instance.html, "<p>hello world</p>")
        self.assertEqual(instance.slug, "test_snippet")
        # test strings
        self.assertEqual(str(instance), "test snippet")

    def test_snippet_ptr_instance(self):
        snippet = Snippet.objects.create(
            name="test snippet",
            html="<p>hello world</p>",
            slug="test_snippet",
        )
        SnippetPtr.objects.create(
            snippet=snippet,
        )
        instance = SnippetPtr.objects.all()
        self.assertEqual(instance.count(), 1)
        instance = SnippetPtr.objects.first()
        # test strings
        self.assertEqual(str(instance), "test snippet")
