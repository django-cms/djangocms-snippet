import logging

from django.conf import settings
from django.db import migrations

from djangocms_versioning.constants import DRAFT

logger = logging.getLogger(__name__)


def forwards(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    # Get the models required for the data migration
    SnippetModel = apps.get_model('djangocms_snippet', 'Snippet')
    SnippetGrouperModel = apps.get_model('djangocms_snippet', 'SnippetGrouper')
    Version = apps.get_model('djangocms_versioning', 'Version')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # The queryset of populate models.
    queryset = SnippetModel.objects.all()
    # The contenttype of the content model
    snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')

    def _create_version(snippet, state=DRAFT, number=1):
        # Get a migration user.
        migration_user = getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID", None)
        if not migration_user:
            logger.warning(
                "Setting DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID not provided, defaulting to user id: 1"
            )
            migration_user = User.objects.get(id=1)

        logger.info("Creating version for new grouper: {}".format(snippet.pk))

        # Create a new version for the snippet
        Version.objects.using(db_alias).create(
            created_by=migration_user,
            state=state,
            number=number,
            object_id=snippet.pk,
            content_type=snippet_contenttype,
        )

    # Iterate over the queryset, create a grouper for each instance and map the content objects foreign key field to it.
    for snippet in queryset:
        grouper = SnippetGrouperModel.objects.create()
        snippet.snippet_grouper = grouper
        snippet.save()
        _create_version(snippet)


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0009_auto_20210811_0942'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
