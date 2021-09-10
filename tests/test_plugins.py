from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from .utils.factories import (
    PageContentWithVersionFactory, SnippetWithVersionFactory,
)


class SnippetPluginsTestCase(CMSTestCase):

    def setUp(self):
        self.language = "en"
        self.superuser = self.get_superuser()
        page_data = {
            "title": "home",
            "template": "page.html",
            "language": self.language,
        }
        self.home_pagecontent = PageContentWithVersionFactory(**page_data)
        self.home = self.home_pagecontent.page
        page_data["title"] = "help"
        self.pagecontent = PageContentWithVersionFactory(**page_data)
        self.page = self.pagecontent.page
        self.pagecontent.versions.first().publish(user=self.superuser)
        self.page.save()

        self.placeholder = self.pagecontent.placeholders.create(slot="content")

    def test_html_rendering(self):
        request_url = self.page.get_absolute_url(self.language) + "?toolbar_off=true"
        snippet = SnippetWithVersionFactory(
            name="plugin_snippet",
            html="<p>Hello World</p>",
            slug="plugin_snippet",
        )
        snippet_grouper = snippet.snippet_grouper
        snippet.versions.last().publish(user=self.get_superuser())
        plugin = add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=snippet_grouper,
        )

        self.assertEqual(plugin.snippet.name, "plugin_snippet")
        self.assertEqual(plugin.snippet.html, "<p>Hello World</p>")
        self.assertEqual(plugin.snippet.slug, "plugin_snippet")

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertIn(b"<p>Hello World</p>", response.content)

    def test_failing_html_rendering(self):
        request_url = self.page.get_absolute_url(self.language) + "?toolbar_off=true"
        snippet = SnippetWithVersionFactory(
            name="plugin_snippet",
            html="{% import weirdness %}",
            slug="plugin_snippet",
        )
        snippet_grouper = snippet.snippet_grouper
        snippet.versions.last().publish(user=self.get_superuser())

        add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=snippet_grouper,
        )

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "Invalid block tag on line 1")
        self.assertContains(response, "Did you forget to register or load this tag?")

    def test_template_rendering(self):
        request_url = self.page.get_absolute_url()
        template = "snippet.html"
        snippet = SnippetWithVersionFactory(
            name="plugin_snippet",
            template=template,
            slug="plugin_snippet",
        )
        snippet_grouper = snippet.snippet_grouper
        snippet.versions.last().publish(user=self.get_superuser())
        plugin = add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=snippet_grouper,
        )

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
        snippet = SnippetWithVersionFactory(
            name="plugin_snippet",
            template=template,
            slug="plugin_snippet",
        )
        snippet_grouper = snippet.snippet_grouper
        snippet.versions.last().publish(user=self.get_superuser())
        add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=snippet_grouper,
        )

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "Template some_template does not exist")
