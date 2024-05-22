#!/usr/bin/env python

try:
    import djangocms_versioning  #NOQA: F401

    add_apps = ['djangocms_versioning']
except ImportError:
    add_apps = []

HELPER_SETTINGS = {
    'SECRET_KEY': "djangocmssnippetstestsuitekey",
    'INSTALLED_APPS': [
        'tests.utils',
        'djangocms_snippet',
        *add_apps,
    ],
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }]
    },
    'LANGUAGE_CODE': 'en',
    'ALLOWED_HOSTS': ['localhost'],
    'DJANGOCMS_SNIPPET_VERSIONING_ENABLED': True,
    'DJANGOCMS_SNIPPET_MODERATION_ENABLED': True,
    'CMS_TEMPLATES': (
        ("page.html", "Normal page"),
    ),
    "DEFAULT_AUTO_FIELD": "django.db.models.AutoField",
    "CMS_CONFIRM_VERSION4": True,
}


def run():
    from app_helper import runner

    runner.cms("djangocms_snippet")


if __name__ == "__main__":
    run()
