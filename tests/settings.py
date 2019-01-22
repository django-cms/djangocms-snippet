#!/usr/bin/env python
# -*- coding: utf-8 -*-
HELPER_SETTINGS = {
    'INSTALLED_APPS': [],
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }]
    },
    'LANGUAGE_CODE': 'en',
    'ALLOWED_HOSTS': ['localhost'],
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_snippet')


if __name__ == '__main__':
    run()
