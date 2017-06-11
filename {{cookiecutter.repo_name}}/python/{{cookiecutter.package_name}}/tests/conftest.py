# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from {{cookiecutter.package_name}}.web import create_app
import pytest


@pytest.fixture(scope='session')
def app():
    ''' fixture for web app testing '''
    app = create_app(debug=True, local=True, use_profiler=False)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    return app
