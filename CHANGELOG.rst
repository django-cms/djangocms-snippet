=========
Changelog
=========

Unreleased
==========


5.0.0
==================
* feat: Universal support for django CMS 3.11 and 4.x


4.1.0 (2024-05-16)
==================

* feat: Added sites support for Snippets
* add support for python 3.10
* add support for django >= 4.2
* drop support for django < 3.2
* drop support python < 3.8


4.0.1.dev2 (2022-11-15)
=======================

* feat: Enable add button to create a snippet when adding a SnippetPlugin


4.0.1.dev1 (2022-05-10)
=======================

* Python 3.8, 3.9 support added
* Django 3.0, 3.1 and 3.2 support added
* Python 3.5 and 3.6 support removed
* Django 1.11 support removed
* port-feat: pre-commit config added from the v3 workstream
* fix: Added test coverage to admin preview view


4.0.0.dev4 (2022-02-03)
=======================

* feat: Preview icon renders form in read only mode


4.0.0.dev3 (2022-01-11)
=======================

* fix: Snippet plugin added to a page now displays name instead of ID
* fix: Slug field on list display for admin should only be displayed when versioning is not available
* fix: Removed unused contents within templates, reducing the clutter within version compare views. Previously this was causing a lot of junk to be included in the version comparison, this will now be reduced.


4.0.0.dev2 (2021-12-22)
=======================

* fix: Removed tight django-treebeard restriction added when 4.5.0 contained breaking changes. The core CMS and django-treebeard have since been patched to resolve the issue.


4.0.0.dev1 (2021-12-14)
=======================

* feat: Exposed the setting DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID as an environment variable for the Divio addon
* fix: Error when rendering a Draft Snippet plugin on a Published page
* fix: Publish snippets by default as they were already in that state pre-versioning and cleanup unnecessary migration files before release!
* feat: djangocms-versioning support added, including model restructure and configuration
* feat: django-cms v4.0.x support added

3.1.1
=====

* fix: Removed tight django-treebeard restriction added when 4.5.0 contained breaking changes. The core CMS and django-treebeard have since been patched to resolve the issue.

3.1.0 2022-09-01
================

* Add support for ace editor loaded from static files through djangocms-static-ace
* Add dark mode support

3.0.0 (2020-09-02)
==================

* Added support for Django 3.1
* Dropped support for Python 2.7 and Python 3.4
* Dropped support for Django < 2.2


2.3.0 (2020-01-29)
==================

* Added support for Django 3.0
* Fixed an issue where render requires a dict instead of a context
* Added ``DJANGOCMS_SNIPPET_CACHE`` cache settings for snippets
* Added further tests to raise coverage
* Fixed smaller issues found during testing
* Fixed alt attribute not rendering correctly
* Fixed missing html variable not present in context


2.2.0 (2019-05-06)
==================

* Added support for Django 2.2 and django CMS 3.7
* Removed support for Django 2.0
* Extended test matrix
* Added isort and adapted imports
* Adapted code base to align with other supported addons
* Exclude ``tests`` folder from release build
* Updated translations


2.1.0 (2018-11-15)
==================

* Added support for Django 1.11, 2.0 and 2.1
* Removed support for Django 1.8, 1.9
* Adapted testing infrastructure (tox/travis) to incorporate
  django CMS 3.5 and 4.0


2.0.0 (2018-01-25)
==================

* Removed reversion references (since they are removed in CMS 3.5)


1.9.2 (2016-11-22)
==================

* Changed naming of ``Aldryn`` to ``Divio Cloud``
* Adapted testing infrastructure (tox/travis) to incorporate
  django CMS 3.4 and dropped 3.2
* Updated translations


1.9.1 (2016-09-08)
==================

* Added a missing migration
* Updated translations


1.9.0 (2016-09-05)
==================

* Added rich text editor
* Added additional files and did some general cleanup
* Removed Django < 1.8 support
* Fixed an issue where fields were restricted to less then 255 characters
* Updated translations


1.8.2 (2016-08-18)
==================

* Use this version for Django < 1.8 support
