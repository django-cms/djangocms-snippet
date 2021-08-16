from django.conf import settings
from django.test import TestCase, override_settings

from djangocms_snippet.utils import is_versioning_enabled


class VersioningConfigurationTestCase(TestCase):

    @override_settings(DJANGOCMS_SNIPPET_VERSIONING_ENABLED=True)
    def test_versioning_enabled_with_setting_config(self):
        # Check getattr returns correct value
        self.assertTrue(getattr(settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED'))

        # Check util is working
        self.assertTrue(is_versioning_enabled())

    def test_versioning_disabled_without_setting_config(self):
        # Check getattr returns None if setting is not configured
        self.assertIsNone(getattr(settings, 'DJANGOCMS_SNIPPET_VERSIONING_ENABLED', None))

        # Util should return false
        self.assertFalse(is_versioning_enabled())
