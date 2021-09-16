from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet.cms_config import snippet_copy_method
from djangocms_snippet.models import Snippet, SnippetGrouper

from .utils.factories import SnippetWithVersionFactory


class VersioningConfigTestCase(CMSTestCase):

    def test_snippet_copy_method(self):
        old_snippet = SnippetWithVersionFactory(
            name="snippet",
            html="<p>Hello World</p>",
            slug="snippet",
        )

        new_snippet = snippet_copy_method(old_snippet)

        self.assertEqual(old_snippet.name, new_snippet.name)
        self.assertEqual(old_snippet.html, new_snippet.html)
        self.assertEqual(old_snippet.snippet_grouper, new_snippet.snippet_grouper)
        self.assertEqual(1, SnippetGrouper.objects.count())
        self.assertEqual(2, Snippet.objects.count())
