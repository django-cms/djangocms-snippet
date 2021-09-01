import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from djangocms_snippet.models import Snippet
from djangocms_versioning.constants import DRAFT
from djangocms_versioning.models import Version


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command to migrate cms3 model structure into cms4 by creating relevant Groupers and Versions'

    def _create_version(self, snippet, state=DRAFT, number=1):
        # Get a migration user.
        migration_user = getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID", None)
        if not migration_user:
            logger.warning(
                "Setting DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID not provided, defaulting to user id: 1"
            )
            migration_user = User.objects.get(id=1)

        # The contenttype of the content model
        snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')

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
        # The queryset of populated models.
        queryset = Snippet._base_manager.all()

        # Since we are doing a database migration, use an atomic transaction
        with transaction.atomic():
            version_count = 0

            for snippet in queryset:
                # If there are no versions of this content, create one.
                if hasattr(snippet, "versions"):
                    if not snippet.versions.all():
                        self._create_version(snippet=snippet)
                        version_count += 1

        logger.info(
            f"Created {version_count} version objects"
        )
