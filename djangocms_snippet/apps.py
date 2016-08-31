# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SnippetConfig(AppConfig):
    name = 'djangocms_snippet'
    verbose_name = _('Snippets')
