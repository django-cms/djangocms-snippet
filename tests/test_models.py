# -*- coding: utf-8 -*-
from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase

from djangocms_snippet.models import Snippet

from django import template


class SnippetTestCase(CMSTestCase):

    def setUp(self):
        self.superuser = self.get_superuser()
        self.page = create_page(
            title="help",
            template="page.html",
            language="en",
        )

    def tearDown(self):
        self.page.delete()

    def test_snippet_instance(self):
        """Snippet instance has been created"""
        Snippet.objects.create(
            name="snippet",
        )
        snippet = Snippet.objects.get(name="snippet")
        self.assertEqual(snippet.name, "snippet")

    def test_html_rendering(self):
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            html="<p>Hello World</p>",
            slug="plugin_snippet",
        )
        plugin = add_plugin(
            self.page.placeholders.get(slot="content"),
            "SnippetPlugin",
            "en",
            snippet=snippet,
        )
        self.assertEqual(plugin.snippet.name, "plugin_snippet")
        self.assertEqual(plugin.snippet.html, "<p>Hello World</p>")
        self.assertEqual(plugin.snippet.slug, "plugin_snippet")

        with self.login_user_context(self.superuser):
            response = self.client.get(self.page.get_absolute_url('en'))

        self.assertIn(b"<p>Hello World</p>", response.content)

    def test_file_rendering(self):
        template = "snippet.html"
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            template=template,
            slug="plugin_snippet",
        )
        plugin = add_plugin(
            self.page.placeholders.get(slot="content"),
            "SnippetPlugin",
            "en",
            snippet=snippet,
        )
        self.assertEqual(plugin.snippet.name, "plugin_snippet")
        self.assertEqual(plugin.snippet.slug, "plugin_snippet")

        with self.login_user_context(self.superuser):
            response = self.client.get(self.page.get_absolute_url('en'))

        self.assertNotIn("Template {} does not exist".format(template).encode(), response.content)
        self.assertNotIn(b"context must be a dict rather than Context", response.content)
        self.assertNotIn(b"context must be a dict rather than PluginContext", response.content)

        # print(dir(response))
        # print(response.content)
        # does not contain Template tests/utils/templates/snippet.html does not exist.
        # does not contain context must be a dict rather than Context.
        # self.assertContains(response, "<p>Hello World Template</p>")

        # print(response.content)

        #self.assertContains(response, "<p>Hello World</p>")
