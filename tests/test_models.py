# -*- coding: utf-8 -*-
from django.test import TestCase

from cms.api import add_plugin, create_page

from djangocms_snippet.models import Snippet


class SnippetTestCase(TestCase):

    def setUp(self):
        self.page = create_page(
            title='help',
            template='page.html',
            language='en',
        )

    def tearDown(self):
        self.page.delete()

    def test_snippet_instance(self):
        """Snippet instance has been created"""
        Snippet.objects.create(
            name='snippet',
        )
        snippet = Snippet.objects.get(name='snippet')
        self.assertEqual(snippet.name, 'snippet')

    def test_plugin_rendering(self):
        pass
        # plugin = add_plugin(
        #     self.page.placeholders.get(slot="content"),
        #     "SnippetPlugin",
        #     "en",
        # )
