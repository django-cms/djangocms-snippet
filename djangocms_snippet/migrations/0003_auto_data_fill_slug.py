# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import Counter

from django.db import models, migrations
from django.utils.text import slugify


def auto_fill_slugs(apps, schema_editor):
    """
    Go through every snippet to fill them a slug if not any
    """
    Snippet = apps.get_model("djangocms_snippet", "Snippet")
    SlugCounter = Counter()
    for snippet_item in Snippet.objects.all():
        if not snippet_item.slug:
            snippet_item.slug = slugify(snippet_item.name)
            # Avoid duplicate slug, adding slug occurence count to the slug
            if snippet_item.slug in SlugCounter:
                snippet_item.slug = "{0}-{1}".format(snippet_item.slug, str(SlugCounter[snippet_item.slug]))
            SlugCounter[snippet_item.slug] += 1
            snippet_item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0002_snippet_slug'),
    ]

    operations = [
        migrations.RunPython(auto_fill_slugs),
    ]
