=========
Changelog
=========

unreleased
==========

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
