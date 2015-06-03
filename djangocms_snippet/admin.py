from .models import Snippet
from django.contrib import admin

class SnippetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ['slug', 'name']
    prepopulated_fields = {"slug": ("name",)}
    #formfield_overrides = {
        #TextField: {'widget': CodeMirrorWidget(config_name='cms_snippet')},
    #}

admin.site.register(Snippet, SnippetAdmin)
