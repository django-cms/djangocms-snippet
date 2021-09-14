from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError

from cms.test_utils.testcases import CMSTestCase

from .utils.factories import SnippetPluginFactory, SnippetWithVersionFactory


class SnippetTemplateTagTestCase(CMSTestCase):

    def test_html_rendered(self):
        snippet = SnippetWithVersionFactory(
            name="test snippet",
            html="<p>hello {{ title }}</p>",
            slug="test_snippet",
        )
        snippet.versions.last().publish(user=self.get_superuser())
        snippet_grouper = snippet.snippet_grouper
        SnippetPluginFactory(snippet_grouper=snippet_grouper, language=["en"])

        context = Context({"title": "world"})
        template_to_render = Template(
            '{% load snippet_tags %}'
            '{% snippet_fragment "test_snippet" %}'
        )
        rendered_template = template_to_render.render(context)

        self.assertInHTML('<p>hello world</p>', rendered_template)

        # test html errors
        context = Context({"title": "world"})
        template_to_render = Template(
            '{% load snippet_tags %}'
            '{% snippet_fragment "test_snippet_2" %}'
        )
        with self.assertRaises(ObjectDoesNotExist):
            # Snippet matching query does not exist.
            rendered_template = template_to_render.render(context)

    def test_template_rendered(self):
        template = "snippet.html"
        snippet = SnippetWithVersionFactory(
            name="test snippet",
            html="<p>hello {{ title }}</p>",
            template=template,
            slug="test_snippet",
        )
        snippet.versions.last().publish(user=self.get_superuser())
        snippet_grouper = snippet.snippet_grouper
        SnippetPluginFactory(snippet_grouper=snippet_grouper, language=["en"])

        # use a string to identify
        context = Context({})
        template_to_render = Template(
            '{% load snippet_tags %}'
            '{% snippet_fragment "test_snippet" %}'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<p>Hello World Template</p>', rendered_template)

        # use an id to identify
        context = Context({})
        template_to_render = Template(
            '{% load snippet_tags %}'
            '{% snippet_fragment 1 %}'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<p>Hello World Template</p>', rendered_template)

        # tests "or" functionality
        context = Context({})
        template_to_render = Template(
            '{% load snippet_tags %}'
            '{% snippet_fragment "test_snippet_1" or %}<p>hello world</p>{% endsnippet_fragment %}'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<p>hello world</p>', rendered_template)

    def test_template_errors(self):
        template = "does_not_exist.html"
        snippet = SnippetWithVersionFactory(
            name="test snippet",
            html="<p>hello {{ title }}</p>",
            template=template,
            slug="test_snippet",
        )
        snippet.versions.last().publish(user=self.get_superuser())
        snippet_grouper = snippet.snippet_grouper
        SnippetPluginFactory(snippet_grouper=snippet_grouper, language=["en"])

        context = Context({})
        template_to_render = Template(
            '{% load snippet_tags %}'
            '{% snippet_fragment "test_snippet" %}'
        )
        rendered_template = template_to_render.render(context)
        self.assertIn('Template does_not_exist.html does not exist.', rendered_template)

        context = Context({})
        template_to_render = Template(
            '{% load snippet_tags %}'
            '{% snippet_fragment "test_snippet_1" %}'
        )
        with self.assertRaises(ObjectDoesNotExist):
            # Snippet object does not exist
            rendered_template = template_to_render.render(context)

        context = Context({})
        with self.assertRaises(TemplateSyntaxError):
            # You need to specify at least a "snippet" ID, slug or instance
            template_to_render = Template(
                '{% load snippet_tags %}'
                '{% snippet_fragment %}'
            )
