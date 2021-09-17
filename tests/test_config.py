from django.apps import apps

from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet.models import Snippet, SnippetGrouper

from .utils.factories import SnippetWithVersionFactory


class VersioningConfigTestCase(CMSTestCase):

    def test_snippet_copy_method(self):
        """
        App should use the default copy method, and return an identical model (apart from PK)
        """
        snippet_cms_config = apps.get_app_config("djangocms_snippet").cms_config
        old_snippet = SnippetWithVersionFactory(
            name="snippet",
            html="<p>Hello World</p>",
            slug="snippet",
        )

        new_snippet = snippet_cms_config.versioning[0].copy_function(old_snippet)

        self.assertNotEqual(old_snippet, new_snippet)
        self.assertEqual(old_snippet.name, new_snippet.name)
        self.assertEqual(old_snippet.html, new_snippet.html)
        self.assertEqual(old_snippet.snippet_grouper, new_snippet.snippet_grouper)
        self.assertEqual(1, SnippetGrouper.objects.count())
        self.assertEqual(2, Snippet._base_manager.count())
