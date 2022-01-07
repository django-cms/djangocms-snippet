import datetime

from cms.api import add_plugin, create_page
from cms.models import PageContent
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.utils import get_object_edit_url, get_object_structure_url

from djangocms_snippet.models import Snippet, SnippetGrouper
from djangocms_versioning.models import Version

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
        result_snippet = plugin.snippet_grouper.snippet(True)

        self.assertEqual(result_snippet.name, "plugin_snippet")
        self.assertEqual(result_snippet.html, "<p>Hello World</p>")
        self.assertEqual(result_snippet.slug, "plugin_snippet")

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
        result_snippet = plugin.snippet_grouper.snippet(True)
        self.assertEqual(result_snippet.name, "plugin_snippet")
        self.assertEqual(result_snippet.slug, "plugin_snippet")

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
        snippet_grouper = SnippetGrouper.objects.create()
        # Create a draft snippet, to be published later
        self.snippet = Snippet.objects.create(
            name="plugin_snippet",
            html="<p>live content</p>",
            slug="plugin_snippet",
            snippet_grouper=snippet_grouper,
        )

        # Publish the snippet
        snippet_version = Version.objects.create(
            content=self.snippet,
            created_by=self.superuser,
            created=datetime.datetime.now()
        )
        snippet_version.publish(user=self.superuser)
        # Copy the snippet to create a draft
        draft_user = self.get_staff_page_user()
        draft_snippet_version = snippet_version.copy(draft_user)
        self.draft_snippet = draft_snippet_version.content
        self.draft_snippet.html = "<p>draft content</p>"
        self.draft_snippet.save()

        # Create a page
        self.page = create_page(
            title="help",
            template="page.html",
            language=self.language,
            created_by=self.superuser,
        )
        # Publish its page content
        self.pagecontent = PageContent._base_manager.filter(page=self.page, language=self.language).first()
        self.pagecontent_version = self.pagecontent.versions.first()
        self.pagecontent_version.publish(self.superuser)

        # Copy our published pagecontent to make a draft
        draft_pagecontent_version = self.pagecontent_version.copy(self.superuser)
        self.draft_pagecontent = draft_pagecontent_version.content

    def test_correct_versioning_state_published_snippet_and_page(self):
        """
        If a page is published, the published snippet should be rendered
        """
        # Add plugin to our published page!
        add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=self.snippet.snippet_grouper,
        )
        # Add plugin to our draft page
        add_plugin(
            self.draft_pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=self.draft_snippet.snippet_grouper,
        )

        # Request for published page
        request_url = self.page.get_absolute_url(self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "<p>live content</p>")
        self.assertNotIn("draft content", str(response.content))

    def test_correct_versioning_state_draft_snippet_and_page(self):
        """
        If we have a draft, the draft snippet should be rendered.
        """
        # Add plugin to our published page!
        add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=self.snippet.snippet_grouper,
        )
        # Add plugin to our draft page
        add_plugin(
            self.draft_pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=self.draft_snippet.snippet_grouper,
        )

        # Request for draft page
        request_url = get_object_edit_url(self.draft_pagecontent, "en")
        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "<p>draft content</p>")
        self.assertNotIn("live content", str(response.content))

    def test_draft_snippet_and_page_live_url_rendering(self):
        """
        If a page is published with a draft snippet created
        nothing should be rendered!
        """
        snippet_grouper = SnippetGrouper.objects.create()
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            html="<p>Draft snippet</p>",
            slug="plugin_snippet",
            snippet_grouper=snippet_grouper,
        )
        Version.objects.create(
            content=snippet,
            created_by=self.superuser,
            created=datetime.datetime.now()
        )

        add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=snippet_grouper,
        )

        request_url = self.page.get_absolute_url(self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Draft snippet", str(response.content))
        self.assertNotIn("Published snippet", str(response.content))

    def test_published_snippet_and_page_live_url_rendering(self):
        """
        If a page is published with a published snippet
        created the snippet should be rendered!
        """
        snippet_grouper = SnippetGrouper.objects.create()
        snippet = Snippet.objects.create(
            name="plugin_snippet",
            html="<p>Published snippet</p>",
            slug="plugin_snippet",
            snippet_grouper=snippet_grouper,
        )
        snippet_version = Version.objects.create(
            content=snippet,
            created_by=self.superuser,
            created=datetime.datetime.now()
        )
        snippet_version.publish(user=self.superuser)

        add_plugin(
            self.pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=snippet_grouper,
        )

        request_url = self.page.get_absolute_url(self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "<p>Published snippet</p>")
        self.assertNotIn("Draft snippet", str(response.content))

    def test_correct_name_is_displayed_for_snippet_component_on_page(self):
        """
        If a component is added to the page, it should show the snippet name and not ID
        """
        add_plugin(
            self.draft_pagecontent.placeholders.get(slot="content"),
            "SnippetPlugin",
            self.language,
            snippet_grouper=self.draft_snippet.snippet_grouper,
        )

        # Request structure endpoint on page
        request_url = get_object_structure_url(self.draft_pagecontent, "en")
        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertContains(response, "<strong>Snippet</strong> plugin_snippet</span>")
