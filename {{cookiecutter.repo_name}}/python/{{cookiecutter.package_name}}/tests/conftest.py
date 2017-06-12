# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from {{cookiecutter.package_name}}.web import create_app
from {{cookiecutter.package_name}}.web.settings import TestConfig, CustomConfig
import pytest


@pytest.fixture(scope='session')
def app():
    ''' fixture for web app testing '''
    object_config = type('Config', (TestConfig, CustomConfig), dict())
    app = create_app(debug=True, local=True, object_config=object_config)
    return app
