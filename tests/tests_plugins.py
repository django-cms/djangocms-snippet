# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.context import Context
from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer

from djangocms_snippet.cms_plugins import SnippetPlugin
from djangocms_snippet.models import Snippet, SnippetPtr


class SnippetTestCase(TestCase):

    def setUp(self):
        self.CONTENT = '<p>Hello World!</p>'
        self.snippet = Snippet(name='My Snippet', html=self.CONTENT, slug='my-snippet')
        self.snippet.save()
        self.faulty_snippet = Snippet(name='Faulty Snippet', html='{% n0w %}', slug='faulty-snippet')
        self.faulty_snippet.save()  

    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            SnippetPlugin,
            'en',
            position='last-child',
            snippet=self.snippet,            
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertIn('content', context)
        self.assertEqual(context['content'], self.CONTENT)

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            SnippetPlugin,
            'en',
            position='last-child',
            snippet=self.snippet,            
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        self.assertEqual(html, self.CONTENT + '\n')

    def test_faulty_plugin_context(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            SnippetPlugin,
            'en',
            position='last-child',
            snippet=self.faulty_snippet,            
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertIn('Invalid block tag', context['content'])
