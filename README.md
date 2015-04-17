djangocms-snippet
=================

A HTML snippet plugin for django CMS.


Installation
------------

This plugin requires `django CMS` 3.0 or higher to be properly installed.

* In your projects `virtualenv`_, run ``pip install djangocms-snippet``.
* Add ``'djangocms_snippet'`` to your ``INSTALLED_APPS`` setting.
* If using Django 1.7 add ``'djangocms_snippet': 'djangocms_snippet.migrations_django',``to ``MIGRATION_MODULES``  (or define ``MIGRATION_MODULES`` if it does not exists); when django CMS 3.1 will be released, migrations for Django 1.7 will be moved to the standard location and the south-style ones to ``south_migrations``.
* Run ``manage.py migrate djangocms_snippet``.

Warning
-------

This plugin should mainly be used during development to quickly test HTML snippets.


    This plugin is a potential security hazard, since it allows admins to place
    custom JavaScript on pages. This may allow administrators with the right to
    add snippets to elevate their privileges to superusers. This plugin should
    only be used during the initial development phase for rapid prototyping and


By default, the contents of a snippet are not searchable when using django-cms's builtin search feature.

To allow the contents of all snippets to be searchable, please set ``DJANGOCMS_SNIPPET_SEARCH`` to ``True`` in your settings.

Translations
------------

If you want to help translate the plugin please do it on transifex:

https://www.transifex.com/projects/p/django-cms/resource/djangocms-snippet/

