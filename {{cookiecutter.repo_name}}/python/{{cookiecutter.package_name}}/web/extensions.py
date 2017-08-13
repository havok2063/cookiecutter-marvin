# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from flask_featureflags import FeatureFlag
from raven.contrib.flask import Sentry
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from flask_profiler import Profiler
import flask_jsglue as jsg
import logging

# JS Glue (allows use of Flask.url_for inside javascript)
jsglue = jsg.JSGlue()

# Feature Flags (allows turning on/off of features)
flags = FeatureFlag()

# Sentry error logging
sentry = Sentry(logging=True, level=logging.ERROR)

# Flask Route Caching
cache = Cache()

# Flask Bcrypt password handling
bcrypt = Bcrypt()

# Flask Profiler
profiler = Profiler()
