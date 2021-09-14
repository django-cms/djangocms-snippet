from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from djangocms_versioning.constants import DRAFT
from djangocms_versioning.models import Version

from djangocms_snippet.models import Snippet


def _create_version(snippet, state=DRAFT, number=1):
    # Get a migration user.
    migration_user = getattr(settings, "DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID", None)
    if not migration_user:
        # If one is not set, default to the first.
        migration_user = User.objects.get(id=1)

    # The contenttype of the content model
    snippet_contenttype = ContentType.objects.get(app_label='djangocms_snippet', model='snippet')

    # Create a new version for the snippet
    Version.objects.create(
        created_by=migration_user,
        state=state,
        number=number,
        object_id=snippet.pk,
        content_type=snippet_contenttype,
    )


class Command(BaseCommand):
    help = 'Command to create versions for snippets'

    def handle(self, *args, **options):
        # The queryset of populated models.
        queryset = Snippet._base_manager.all()

        # Since we are doing a database migration, use an atomic transaction
        with transaction.atomic():
            # Iterate over snippet groupers, get the last snippet, and create a version for it if one doesn't exist
            for snippet in queryset:
                if not snippet.versions.all():
                    _create_version(snippet=snippet)
