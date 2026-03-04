import os

SECRET_KEY = "djangocmssnippetstestsuitekey"

ALLOWED_HOSTS = ["localhost"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.messages",
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    "djangocms_versioning",
    "djangocms_snippet",
    "tests.utils",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join((os.path.dirname(__file__)), "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

SITE_ID = 1

CMS_TEMPLATES = (("page.html", "Normal page"),)

CMS_LANGUAGES = {
    1: [
        {
            "code": "en",
            "name": "English",
        }
    ]
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {
            # disable migrations when creating test database
            "MIGRATE": False,
        },
    }
}

CMS_CONFIRM_VERSION4 = True

USE_TZ = True

LANGUAGE_CODE = "en"

DJANGOCMS_SNIPPET_VERSIONING_ENABLED = True
DJANGOCMS_SNIPPET_MODERATION_ENABLED = True

ROOT_URLCONF = "tests.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
