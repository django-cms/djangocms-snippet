djangocms-snippet
=================

A HTML snippet plugin for django CMS.


Installation
------------

This plugin requires `django CMS` 3.0 or higher to be properly installed.

* In your projects `virtualenv`_, run ``pip install djangocms-snippet``.
* Add ``'djangocms_snippet'`` to your ``INSTALLED_APPS`` setting.
* Run ``manage.py migrate djangocms_snippet``.

Warning
-------

This plugin should mainly be used during development to quickly test HTML snippets.


    This plugin is a potential security hazard, since it allows admins to place
    custom JavaScript on pages. This may allow administrators with the right to
    add snippets to elevate their privileges to superusers. This plugin should
    only be used during the initial development phase for rapid prototyping and


Translations
------------

If you want to help translate the plugin please do it on transifex:

https://www.transifex.com/projects/p/django-cms/resource/djangocms-snippet/

