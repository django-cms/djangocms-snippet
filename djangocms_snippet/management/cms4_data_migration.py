import logging

from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from djangocms_versioning.models import Version

from djangocms_snippet.models import Snippet, SnippetGrouper

from djangocms_versioning.constants import DRAFT


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command to migrate cms3 model structure into cms4 by creating relevant Groupers and Versions'

    def _create_version(snippet, state=DRAFT, number=1):
        # Get a migration user.
        migration_user = getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID", None)
        # The contenttype of the content model
        snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')

        if not migration_user:
            logger.warning(
                "Setting DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID not provided, defaulting to user id: 1"
            )
            migration_user = User.objects.get(id=1)

        logger.info("Creating version for new grouper: {}".format(snippet.pk))

        # Create a new version for the snippet
        Version.objects.create(
            created_by=migration_user,
            state=state,
            number=number,
            object_id=snippet.pk,
            content_type=snippet_contenttype,
        )

    def handle(self, *args, **options):
        # The queryset of populate models.
        queryset = Snippet.objects.all()

        # Iterate over the queryset, create a grouper for each instance
        # and map the content objects foreign key field to it.
        for snippet in queryset:
            if not snippet.snippet_grouper:
                grouper = SnippetGrouper.objects.create()
                snippet.snippet_grouper = grouper
                snippet.save()
                if not snippet.versions.all():
                    self._create_version(snippet)
