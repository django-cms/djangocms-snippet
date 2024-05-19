from django.conf import settings
from django.db import models

from cms import __version__ as cms_version


if cms_version < "4":
    class Version(models.Model):
        content = models.ForeignKey("djangocms_snippet.Snippet", related_name="versions", on_delete=models.CASCADE)
        created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        )
        state = models.CharField(max_length=50, default="draft")

        def __init__(self, *args, **kwargs):
            kwargs.pop("content_type", None)
            obj_id = kwargs.pop("object_id", None)
            if obj_id:
                kwargs["content_id"] = obj_id
            super().__init__(*args, **kwargs)


        def publish(self, user):
            pass
