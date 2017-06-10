# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from flask import Flask, Blueprint
from flask import session, request, render_template, g, jsonify
import flask_jsglue as jsg
from inspect import getmembers, isfunction
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
    from marvin.web.controllers.index import index
    # from marvin.web.controllers.galaxy import galaxy
    # from marvin.web.controllers.search import search
    # from marvin.web.controllers.plate import plate
    # from marvin.web.controllers.images import images
    # from marvin.web.controllers.users import users

    # ----------------------------------
    # Create App
    app_base = os.environ.get('{{cookiecutter.package_name|upper}}_BASE', {{cookiecutter.package_name}})
    app = Flask(__name__, static_url_path='/{0}/static'.format(app_base))
    api = Blueprint("api", __name__, url_prefix='/{0}/api'.format(app_base))
    app.debug = debug
    jsg.JSGLUE_JS_PATH = '/{0}/jsglue.js'.format(app_base)
    jsglue = jsg.JSGlue(app)


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


    # ----------------
    # Error Handling
    # ----------------



    # ----------------------------------
    # Registration
    #
    # API route registration


    # Web route registration
    app.register_blueprint(index, url_prefix=url_prefix)

    # Register all custom Jinja filters in the file.
    #app.register_blueprint(jinjablue)

    # Register error handlers
    #app.register_blueprint(web)

    return app
