# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from flask import Flask, Blueprint
from flask import session, request, render_template, g, jsonify
from inspect import getmembers, isfunction
from {{cookiecutter.package_name}}.web.controllers import index
from {{cookiecutter.package_name}}.web.jinja_filters import jinjablue
from {{cookiecutter.package_name}}.web.error_handlers import errors
from {{cookiecutter.package_name}}.web.extensions import jsglue, flags, sentry
from {{cookiecutter.package_name}}.web.settings import ProdConfig, DevConfig, CustomConfig
from {{cookiecutter.package_name}}.api.index import MainView
import sys
import os
import logging

# ================================================================================


def create_app(debug=False, local=False, object_config=None):
    ''' Creates and runs the app '''

    # ----------------------------------
    # Create App
    app_base = os.environ.get('{{cookiecutter.package_name|upper}}_BASE', '{{cookiecutter.package_name}}')
    app = Flask(__name__, static_url_path='/{0}/static'.format(app_base))
    api = Blueprint("api", __name__, url_prefix='/{0}/api'.format(app_base))
    app.debug = debug

    # ----------------------------------
    # Initialize logging + Sentry + UWSGI config for Production Marvin


    # Find which connection to make
    # connection = getDbMachine()
    # local = (connection == 'local') or local

    # ----------------------------------
    # Set some environment variables
    # os.environ['SAS_REDUX'] = 'sas/mangawork/manga/spectro/redux'
    # os.environ['SAS_ANALYSIS'] = 'sas/mangawork/manga/spectro/analysis'
    # os.environ['SAS_SANDBOX'] = 'sas/mangawork/manga/sandbox'
    # release = os.environ.get('MARVIN_RELEASE', 'mangawork')
    # os.environ['SAS_PREFIX'] = 'marvin2' if release == 'mangawork' else 'dr13/marvin'
    url_prefix = '/{{cookiecutter.package_name}}' if local else '/{0}'.format(app_base)

    # ----------------------------------
    # Load the appropriate Flask configuration file for debug or production
    if not object_config:
        if app.debug or local:
            app.logger.info('Loading Development Config!')
            object_config = type('Config', (DevConfig, CustomConfig), dict())
        else:
            app.logger.info('Loading Production Config!')
            object_config = type('Config', (ProdConfig, CustomConfig), dict())
    app.config.from_object(object_config)

    # ------------
    # Registration
    register_extensions(app, app_base=app_base)
    register_api(app, api)
    register_blueprints(app, url_prefix=url_prefix)

    return app


def register_api(app, api):
    ''' Register the Flask API routes used '''

    MainView.register(api)
    app.register_blueprint(api)


def register_extensions(app, app_base=None):
    ''' Register the Flask extensions used '''

    jsglue.JSGLUE_JS_PATH = '/{0}/jsglue.js'.format(app_base)
    jsglue.init_app(app)
    flags.init_app(app)
    if app.config.USE_SENTRY:
        sentry.init_app(app)

    # Initialize the Flask-Profiler ; see results at localhost:portnumber/app_base/flask-profiler
    if app.config.USE_PROFILER:
        try:
            flask_profiler.init_app(app)
        except Exception as e:
            pass


def register_blueprints(app, url_prefix=None):
    ''' Register the Flask Blueprints used '''

    app.register_blueprint(index.indexblue, url_prefix=url_prefix)
    app.register_blueprint(jinjablue)
    app.register_blueprint(errors)



