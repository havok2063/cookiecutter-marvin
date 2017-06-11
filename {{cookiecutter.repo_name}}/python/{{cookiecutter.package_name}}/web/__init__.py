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
from {{cookiecutter.package_name}}.web.extensions import jsglue
import sys
import os
import logging

# ================================================================================


def create_app(debug=False, local=False, use_profiler=True):
    ''' Creates and runs the app '''

    # from marvin.api.cube import CubeView
    # from marvin.api.maps import MapsView
    # from marvin.api.modelcube import ModelCubeView
    # from marvin.api.plate import PlateView
    # from marvin.api.rss import RSSView
    # from marvin.api.spaxel import SpaxelView
    # from marvin.api.query import QueryView
    # from marvin.api.general import GeneralRequestsView


    # ----------------------------------
    # Create App
    app_base = os.environ.get('{{cookiecutter.package_name|upper}}_BASE', '{{cookiecutter.package_name}}')
    app = Flask(__name__, static_url_path='/{0}/static'.format(app_base))
    api = Blueprint("api", __name__, url_prefix='/{0}/api'.format(app_base))
    app.debug = debug

    # ----------------------------------
    # Initialize logging + Sentry + UWSGI config for Production Marvin
    if app.debug is False:

        # --------------------------------------
        # Configuration when running under uWSGI
        try:
            import uwsgi
            app.use_x_sendfile = True
        except ImportError:
            pass

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
    if app.debug:
        if local:
            server_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration', 'localhost.cfg')
        else:
            server_config_file = None
            app.logger.debug("Trying to run in debug mode, but not running on a development machine that has database access.")
            # sys.exit(1)
    else:
        try:
            import uwsgi
            server_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration', uwsgi.opt['flask-config-file'])
        except ImportError:
            app.logger.debug("Trying to run in production mode, but not running under uWSGI. You might try running again with the '--debug' flag.")
            sys.exit(1)

    if server_config_file:
        app.logger.info('Loading config file: {0}'.format(server_config_file))
        app.config.from_pyfile(server_config_file)

    # ----------------------------------
    # Initialize feature flags
    # feature_flags = FeatureFlag(app)
    # configFeatures(debug=app.debug)

    # Update any config parameters
    # app.config["UPLOAD_FOLDER"] = os.environ.get("MARVIN_DATA_DIR", None)
    # app.config["LIB_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')




    #
    # API route registration

    # Registration
    # ------------
    register_extensions(app, app_base=app_base)
    register_api(app)
    register_blueprints(app, url_prefix=url_prefix)

    return app


def register_api(app):
    ''' Register the Flask API routes used '''


def register_extensions(app, app_base=None):
    ''' Register the Flask extensions used '''
    jsglue.JSGLUE_JS_PATH = '/{0}/jsglue.js'.format(app_base)
    jsglue.init_app(app)


def register_blueprints(app, url_prefix=None):
    ''' Register the Flask Blueprints used '''

    app.register_blueprint(index.indexblue, url_prefix=url_prefix)
    app.register_blueprint(jinjablue)
    app.register_blueprint(errors)



