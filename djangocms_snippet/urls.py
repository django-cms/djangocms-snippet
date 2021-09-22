from django.conf.urls import url
from django.urls import include, path

from cms.views import render_object_preview

from djangocms_snippet.models import Snippet
from djangocms_snippet.views import SnippetPreviewView


urlpatterns = [
    url(
        r"^(?P<snippet_id>\d+)/preview/$",
        SnippetPreviewView.as_view(),
        name=f"{Snippet._meta.app_label}_{Snippet._meta.model_name}_preview"
        )
]
