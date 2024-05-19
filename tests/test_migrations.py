# original from
# http://tech.octopus.energy/news/2016/01/21/testing-for-missing-migrations-in-django.html
from io import StringIO
from unittest import skipIf

from django.core.management import call_command
from django.test import TestCase, override_settings

from cms import __version__ as cms_version


class MigrationTestCase(TestCase):

    @skipIf(cms_version.startswith("4.0."), 'This test fails on django-cms 4.0')
    @override_settings(MIGRATION_MODULES={})
    def test_for_missing_migrations(self):
        output = StringIO()
        options = {
            'interactive': False,
            'dry_run': True,
            'stdout': output,
            'check_changes': True,
        }

        try:
            call_command("makemigrations", "djangocms_snippet", **options)
        except SystemExit as e:
            status_code = str(e)
        else:
            # the "no changes" exit code is 0
            status_code = '0'

        if status_code == '1':
            self.fail('There are missing migrations:\n {}'.format(output.getvalue()))
