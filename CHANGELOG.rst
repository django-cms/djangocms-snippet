=========
Changelog
=========


2.1.1 (unreleased)
==================

* Extended test matrix
* Added isort and adapted imports
* Adapted code base to align with other supported addons
* Exclude ``tests`` folder from release build


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
