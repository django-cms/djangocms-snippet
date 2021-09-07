from django.db import migrations

from djangocms_snippet.conf import DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID

try:
    from djangocms_versioning.constants import DRAFT
    djangocms_versioning_enabled = True
except:
    djangocsm_versioning_enabled = False


def cms4_grouper_version_migration(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Snippet = apps.get_model("djangocms_snippet", "Snippet")
    SnippetGrouper = apps.get_model("djangocms_snippet", "SnippetGrouper")
    User = apps.get_model('auth', 'User')

    snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')
    snippet_queryset = Snippet.objects.all()

    for snippet in snippet_queryset:
        grouper = SnippetGrouper.objects.create()
        snippet.new_snippet = grouper
        snippet.save()

        # Get a migration user.
        migration_user = User.objects.get(id=DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID)

        if djangocsm_versioning_enabled:
            Version = apps.get_model("djangocms_versioning", "Version")
            Version.objects.create(
                created_by=migration_user,
                state=DRAFT,
                number=1,
                object_id=snippet.pk,
                content_type=snippet_contenttype,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0009_auto_20210831_0715'),
    ]

    operations = [
        migrations.RunPython(cms4_grouper_version_migration)
    ]
