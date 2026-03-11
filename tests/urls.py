from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path

i18n_urls = [
    re_path(r"^admin/", admin.site.urls),
    path("", include("cms.urls")),
]

urlpatterns = i18n_patterns(*i18n_urls)
