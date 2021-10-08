from cms.test_utils.testcases import CMSTestCase
from cms.utils.urlutils import admin_reverse

from .utils.factories import SnippetWithVersionFactory


class PreviewViewTestCase(CMSTestCase):
    def setUp(self):
        self.snippet = SnippetWithVersionFactory(html="<h1>Test Title</h1><br><p>Test paragraph</p>")
        self.preview_url = admin_reverse(
            "djangocms_snippet_snippet_preview",
            kwargs={"snippet_id": self.snippet.id},
        )

    def test_preview_renders_html(self):
        self.snippet.versions.last().publish(user=self.get_superuser())
        with self.login_user_context(self.get_superuser()):
            response = self.client.get(self.preview_url)

        self.assertEqual(self.snippet.html, "<h1>Test Title</h1><br><p>Test paragraph</p>")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Test Title</h1><br><p>Test paragraph</p>")
