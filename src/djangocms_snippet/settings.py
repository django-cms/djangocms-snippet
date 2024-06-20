#!/usr/bin/env python
HELPER_SETTINGS = {
    "SECRET_KEY": "djangocmssnippetstestsuitekey",
    "INSTALLED_APPS": [
        "tests.utils",
        "djangocms_versioning",
        "djangocms_snippet",
    ],
    "CMS_LANGUAGES": {
        1: [
            {
                "code": "en",
                "name": "English",
            }
        ]
    },
    "LANGUAGE_CODE": "en",
    "ALLOWED_HOSTS": ["localhost"],
    "DJANGOCMS_SNIPPET_VERSIONING_ENABLED": True,
    "DJANGOCMS_SNIPPET_MODERATION_ENABLED": True,
    "CMS_TEMPLATES": (("page.html", "Normal page"),),
    "DEFAULT_AUTO_FIELD": "django.db.models.AutoField",
}


def run():
    from app_helper import runner

    runner.cms("djangocms_snippet")


if __name__ == "__main__":
    run()
