from collections import Counter
import typing

from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from django.utils.text import slugify


def auto_fill_slugs(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """
    Go through every snippet to fill them a slug if not any
    """
    Snippet = apps.get_model("djangocms_snippet", "Snippet")
    SlugCounter: typing.Counter[str] = Counter()
    for snippet_item in Snippet.objects.all():  # pragma: no cover
        if not snippet_item.slug:
            snippet_item.slug = slugify(snippet_item.name)
            # Avoid duplicate slug, adding slug occurrence count to the slug
            if snippet_item.slug in SlugCounter:
                snippet_item.slug = f"{snippet_item.slug}-{str(SlugCounter[snippet_item.slug])}"
            SlugCounter[snippet_item.slug] += 1
            snippet_item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0002_snippet_slug'),
    ]

    operations = [
        migrations.RunPython(auto_fill_slugs),
    ]
