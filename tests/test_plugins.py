from cms.api import add_plugin, create_page, create_title
from cms.models import PageContent
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.utils import get_object_edit_url

from .utils.factories import SnippetWithVersionFactory


class SnippetPluginsTestCase(CMSTestCase):

    def setUp(self):
        self.language = "en"
        self.superuser = self.get_superuser()
        self.page = create_page(
            title="help",
            template="page.html",
            language=self.language,
            created_by=self.superuser,
        )
        # Publish our page content
        self.pagecontent = PageContent._base_manager.filter(page=self.page, language=self.language).first()
        version = self.pagecontent.versions.first()
        version.publish(self.superuser)

    def tearDown(self):
        self.page.delete()
        self.superuser.delete()

    def test_html_rendering(self):
        snippet = SnippetWithVersionFactory(
            name="plugin_snippet",
            html="<p>Hello World</p>",
            slug="plugin_snippet",
        )
        snippet_grouper = snippet.snippet_grouper
        plugin = add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=snippet_grouper,
        )

        snippet.versions.last().publish(user=self.get_superuser())
        request_url = self.page.get_absolute_url("en")

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


class SnippetPluginVersioningRenderTestCase(CMSTestCase):
    def setUp(self):
        self.language = "en"
        self.superuser = self.get_superuser()
        self.page = create_page(
            title="help",
            template="page.html",
            language=self.language,
            created_by=self.superuser,
        )
        # Create a draft snippet, to be published later
        self.snippet = SnippetWithVersionFactory(
            name="plugin_snippet",
            html="<p>Hello World</p>",
            slug="plugin_snippet",
        )

    def test_correct_versioning_state_published_snippet_and_page(self):
        """
        If a page is published, the published snippet should be rendered, whereas if we have a draft, the draft snippet
        should be rendered.
        """
        # Publish our page content
        self.pagecontent = PageContent._base_manager.filter(page=self.page, language=self.language).first()
        version = self.pagecontent.versions.first()
        version.publish(self.superuser)
        # Publish the snippet
        self.snippet.versions.first().publish(user=self.superuser)
        published_pagecontent = self.page.pagecontent_set.first()
        # Add plugin to our published page!
        add_plugin(
            published_pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=self.snippet.snippet_grouper,
        )
        # Request for published page
        request_url = self.page.get_absolute_url(self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "<p>Hello World</p>")

    def test_correct_versioning_state_draft_snippet_and_page(self):
        """
        If a page is published, the published snippet should be rendered, whereas if we have a draft, the draft snippet
        should be rendered.
        """
        # Create the draft page content with a different html value
        self.snippet.html = "<h1>Hello World</h1>"
        self.snippet.save()
        draft_pagecontent = create_title("en", "Snippet Test Page", self.page, created_by=self.superuser)
        # Add plugin to our draft page
        add_plugin(
            draft_pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=self.snippet.snippet_grouper,
        )
        # Request for published page
        request_url = get_object_edit_url(draft_pagecontent, "en")
        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "<h1>Hello World</h1>")
