# -*- coding: utf-8 -*-

from .models import Snippet
from django.contrib import admin


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ['slug', 'name']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Snippet, SnippetAdmin)
