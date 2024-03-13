#!/usr/bin/env python
import os
import sys
from setuptools import find_packages, setup

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from djangocms_snippet import __version__
  

REQUIREMENTS = [
    'django-cms',
    'django-treebeard>=4.3',
]


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Framework :: Django',
    'Framework :: Django :: 3.2',
    'Framework :: Django :: 4.2',
    'Framework :: Django CMS',
    'Framework :: Django CMS :: 4.0',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


setup(
    name='djangocms-snippet',
    version=__version__,
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/divio/djangocms-snippet',
    license='BSD-3-Clause',
    description='Adds snippet plugin to django CMS.',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)
