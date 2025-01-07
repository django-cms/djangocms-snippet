==================
django CMS Snippet
==================

|pypi| |coverage| |python| |django| |djangocms| |djangocms4|


**django CMS Snippet** provides a plugin for `django CMS <http://django-cms.org>`_
to inject HTML, CSS or JavaScript snippets into your website.

This project is endorsed by the `django CMS Association <https://www.django-cms.org/en/about-us/>`_. Join us on `Slack <https://www.django-cms.org/slack/>`_.



Warning: We recommend using this plugin only during development::

    This plugin is a potential security hazard, since it allows authorized-
    users to place custom markup or Javascript on pages bypassing all of
    Django's normal sanitization mechanisms. This could be exploited by users
    with the right to add snippets to elevate their privileges to superusers.
    This plugin should only be used during the initial development phase for
    rapid prototyping and testing.

.. image:: preview.gif


*******************************************
Contribute to this project and win rewards
*******************************************

Because this is a an open-source project, we welcome everyone to
`get involved in the project <https://www.django-cms.org/en/contribute/>`_ and
`receive a reward <https://www.django-cms.org/en/bounty-program/>`_ for their contribution.
Become part of a fantastic community and help us make django CMS the best CMS in the world.

We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/django-cms/djangocms-snippet/graphs/contributors>`_
section.

One of the easiest contributions you can make is helping to translate this addon on
`Transifex <https://www.transifex.com/projects/p/djangocms-snippet/>`_.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/djangocms-snippet/blob/master/setup.py>`_
file for additional dependencies.


Installation
------------

For a manual install:

* run ``pip install djangocms-snippet``
* add ``djangocms_snippet`` to your ``INSTALLED_APPS``
* run ``python manage.py migrate djangocms_snippet``

Djangocms-snippet uses the ace code editor which normally is loaded from a CDN.
If you prefer your application to provide the editor locally, you can change
the requirement from `djangocms_snippet` to `djangocms_snippet[static-ace]` and
add `djangocms_static_ace` to your project's `INSTALLED_APPS`.


Configuration
-------------

To allow the contents of all snippets to be searchable, please set
``DJANGOCMS_SNIPPET_SEARCH`` to ``True`` in your settings::

    DJANGOCMS_SNIPPET_SEARCH = True

We are using `Ace <https://ace.c9.io/#nav=about>`_ as our editor of choice
to edit the snippet content. You can customize the
`theme <https://github.com/ajaxorg/ace/tree/master/lib/ace/theme>`_ and
`mode <https://github.com/ajaxorg/ace/tree/master/lib/ace/mode>`_ through::

    DJANGOCMS_SNIPPET_THEME = 'github'
    DJANGOCMS_SNIPPET_MODE = 'html'

If dynamic content is inserted (for example ``{% show_menu ... %}``), the plugin cache must be disabled,
please set ``DJANGOCMS_SNIPPET_CACHE`` to ``False`` in your settings::

    DJANGOCMS_SNIPPET_CACHE = False # default value is False

Migration 0010 requires the use of a user in order to create versions for existing snippets (if djangocms_versioning is installed and enabled),
a user can be chosen with the setting ``DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID``, the default is 1.
This setting is also exposed as an Environment variable for Divio projects using the Divio addon.

    DJANGOCMS_SNIPPET_VERSIONING_MIGRATION_USER_ID = 2 # Will use user with id: 2

Template tag
------------

You can also use a template tag to render a snippet rather than a plugin::

    {% load snippet_tags %}
    {% snippet_fragment [reference] %}

Replace ``[reference]`` with either:

* The snippet ID, e.g. ``{% snippet_fragment 42 %}``
* The snippet slug, e.g. ``{% snippet_fragment 'my-snippet' %}``
* The snippet instance, e.g. ``{% snippet_fragment instance.snippet %}``

Optionally provide a fallback if there is no matching id/slug/instance::

    {% snippet_fragment 'my-snippet' or %}
        ... your content fallback here ...
    {% endsnippet_fragment %}


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


.. |pypi| image:: https://badge.fury.io/py/djangocms-snippet.svg
    :target: http://badge.fury.io/py/djangocms-snippet
.. |coverage| image:: https://codecov.io/gh/django-cms/djangocms-snippet/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/django-cms/djangocms-snippet
.. |python| image:: https://img.shields.io/badge/python-3.9+-blue.svg
    :target: https://pypi.org/project/djangocms-snippet/
.. |django| image:: https://img.shields.io/badge/django-4.2+-blue.svg
    :target: https://www.djangoproject.com/
.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.11-blue.svg
    :target: https://www.django-cms.org/
.. |djangocms4| image:: https://img.shields.io/badge/django%20CMS-4%2B-blue.svg
    :target: https://www.django-cms.org/
