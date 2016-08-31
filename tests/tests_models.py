# -*- coding: utf-8 -*-
from django.test import TestCase

from djangocms_snippet.models import Snippet


class SnippetTestCase(TestCase):

    def setUp(self):
        Snippet.objects.create(
            name='snippet',
        )

    def test_snippet_instance(self):
        """Snippet instance has been created"""
        snippet = Snippet.objects.get(name='snippet')
        self.assertEqual(snippet.name, 'snippet')
