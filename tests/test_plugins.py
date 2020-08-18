from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet.models import Snippet


class SnippetPluginsTestCase(CMSTestCase):

    def setUp(self):
        self.language = "en"
        self.home = create_page(
            title="home",
            template="page.html",
            language=self.language,
        )
        self.home.publish(self.language)
        self.page = create_page(
            title="help",
            template="page.html",
            language=self.language,
        )
        self.page.publish(self.language)
        self.placeholder = self.page.placeholders.get(slot="content")
        self.superuser = self.get_superuser()

    def tearDown(self):
        self.page.delete()
        self.home.delete()
        self.superuser.delete()

    def test_html_rendering(self):
        request_url = self.page.get_absolute_url(self.language) + "?toolbar_off=true"
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            html="<p>Hello World</p>",
            slug="plugin_snippet",
        )
        plugin = add_plugin(
            self.page.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet=snippet,
        )
        self.page.publish(self.language)
        self.assertEqual(plugin.snippet.name, "plugin_snippet")
        self.assertEqual(plugin.snippet.html, "<p>Hello World</p>")
        self.assertEqual(plugin.snippet.slug, "plugin_snippet")

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertIn(b"<p>Hello World</p>", response.content)

    def test_failing_html_rendering(self):
        request_url = self.page.get_absolute_url(self.language) + "?toolbar_off=true"
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            html="{% import weirdness %}",
            slug="plugin_snippet",
        )
        add_plugin(
            self.page.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet=snippet,
        )
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "Invalid block tag on line 1")
        self.assertContains(response, "Did you forget to register or load this tag?")

    def test_template_rendering(self):
        request_url = self.page.get_absolute_url(self.language) + "?toolbar_off=true"
        template = "snippet.html"
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            template=template,
            slug="plugin_snippet",
        )
        snippet.save()
        plugin = add_plugin(
            self.page.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet=snippet,
        )
        self.page.publish(self.language)
        self.assertEqual(plugin.snippet.name, "plugin_snippet")
        self.assertEqual(plugin.snippet.slug, "plugin_snippet")

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertNotIn("Template {} does not exist".format(template).encode(), response.content)
        self.assertNotIn(b"context must be a dict rather than Context", response.content)
        self.assertNotIn(b"context must be a dict rather than PluginContext", response.content)
        self.assertContains(response, "<p>Hello World Template</p>")

    def test_failing_template_rendering(self):
        request_url = self.page.get_absolute_url(self.language) + "?toolbar_off=true"
        template = "some_template"
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            template=template,
            slug="plugin_snippet",
        )
        snippet.save()
        add_plugin(
            self.page.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet=snippet,
        )
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "Template some_template does not exist")
