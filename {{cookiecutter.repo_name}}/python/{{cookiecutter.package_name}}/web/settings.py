# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
import os


class Config(object):
    SECRET_KEY = os.environ.get('{{cookiecutter.package_name|upper}}_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    APP_BASE = os.environ.get('{{cookiecutter.package_name|upper}}_BASE', '{{cookiecutter.package_name}}')
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir, os.pardir, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''
    GOOGLE_ANALYTICS = ''
    LOG_SQL_QUERIES = True
    FEATURE_FLAGS_NEW = True
    UPLOAD_FOLDER = os.environ.get("{{cookiecutter.package_name|upper}}_DATA_DIR", '/tmp/')
    ALLOWED_EXTENSIONS = set(['txt', 'csv'])
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'wtfsecretkey'
    USE_PROFILER = True  # Use the Flask Profiler Extension
    USE_SENTRY = False  # Turn off Sentry error logging
    FLASK_PROFILER = {
        "enabled": True,
        "storage": {
            "engine": "sqlite",
            "FILE": os.path.join(PROJECT_ROOT, 'flask_profiler.sql')
        },
        'endpointRoot': '{0}/profiler'.format(APP_BASE),
        "basicAuth": {
            "enabled": True,
            "username": "admin",
            "password": "admin"
        }
    }


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    USE_X_SENDFILE = True
    USE_SENTRY = True
    SENTRY_DSN = os.environ.get('SENTRY_DSN', None)


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    USE_PROFILER = False  # Turn off the Flask Profiler extension


class CustomConfig(object):
    ''' Project specific configuration.  Always gets appended to an above Config class '''
    pass


