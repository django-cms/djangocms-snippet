djangocms-snippet
=================

A HTML snippet plugin for django CMS.


Installation
------------

This plugin requires `django CMS` 3.0 or higher to be properly installed.

* In your projects `virtualenv`, run ``pip install djangocms-snippet``.
* Add ``'djangocms_snippet'`` to your ``INSTALLED_APPS`` setting.
* If using Django 1.6 and South < 1.0.2 add ``'djangocms_snippet': 'djangocms_snippet.migrations_django',``
  to ``SOUTH_MIGRATION_MODULES`` (or define ``SOUTH_MIGRATION_MODULES`` if it 
  does not exist).
* Run ``manage.py migrate djangocms_snippet``.

Warning
-------

This plugin should mainly be used during development to quickly test
HTML snippets.::

    This plugin is a potential security hazard, since it allows authorized-
    users to place custom markup or Javascript on pages bypassing all of
    Django's normal sanitization mechanisms. This could be exploited by users
    with the right to add snippets to elevate their privileges to superusers.
    This plugin should only be used during the initial development phase for
    rapid prototyping and testing. 

By default, the contents of a snippet are not searchable when using django-cms's
builtin search feature.

To allow the contents of all snippets to be searchable, please set
``DJANGOCMS_SNIPPET_SEARCH`` to ``True`` in your settings.

Template tags
-------------

There is a template tag you can use in your templates even out of the CMS templates:

    {% load snippet_tags %}
    {% snippet_fragment [Snippet ID or slug or instance] %}

The first argument is required, you can use either:

* The Snippet ID;
* The Snippet slug;
* The Snippet instance.

Target your snippet using its ID (a number):

    {% load snippet_tags %}
    {% snippet_fragment 42 %}

Or with its slug (a string):

    {% load snippet_tags %}
    {% snippet_fragment 'my-snippet' %}

Finally, instead of the ID or slug, you can directly give a snippet instance.

Also you can use it as a template block giving a content fallback::

    {% snippet_fragment 'my-snippet' or %}
        ... your content fallback here ...
    {% endsnippet_fragment %}

In case there is no matched snippet for the given instance/id/slug, content fallback will be rendered instead.

Translations
------------

If you want to help translate the plugin please do it on transifex:

https://www.transifex.com/projects/p/django-cms/resource/djangocms-snippet/
