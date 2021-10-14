from cms.test_utils.testcases import CMSTestCase
from cms.utils.urlutils import admin_reverse

from .utils.factories import SnippetWithVersionFactory


class PreviewViewTestCase(CMSTestCase):
    def setUp(self):
        self.snippet = SnippetWithVersionFactory(html="<h1>Test Title</h1><br><p>Test paragraph</p>")
        self.user = self.get_superuser()

    def test_preview_renders_html(self):
        """
        Check that our snippet HTML is rendered, unescaped, on the page
        """
        preview_url = admin_reverse(
            "djangocms_snippet_snippet_preview",
            kwargs={"snippet_id": self.snippet.id},
        )
        with self.login_user_context(self.user):
            response = self.client.get(preview_url)

        self.assertEqual(self.snippet.html, "<h1>Test Title</h1><br><p>Test paragraph</p>")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Test Title</h1><br><p>Test paragraph</p>")

    def test_preview_raises_404_no_snippet(self):
        """
        With no Snippet to preview, a 404 will be raised
        """
        preview_url = admin_reverse(
            "djangocms_snippet_snippet_preview",
            kwargs={"snippet_id": 999},  # Non existent PK!
        )
        with self.login_user_context(self.user):
            response = self.client.get(preview_url)

        self.assertEqual(response.status_code, 404)
