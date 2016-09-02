# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.db import models
from django.forms import Textarea

from .models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ['slug', 'name']
    prepopulated_fields = {'slug': ('name',)}
    change_form_template = 'djangocms_snippet/admin/change_form.html'
    text_area_attrs = {
        'rows': 20,
        'data-editor': True,
        'data-mode': getattr(settings, 'DJANGOCMS_SNIPPET_THEME', 'html'),
        'data-theme': getattr(settings, 'DJANGOCMS_SNIPPET_MODE', 'github'),
    }

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs=text_area_attrs)}
    }


admin.site.register(Snippet, SnippetAdmin)
