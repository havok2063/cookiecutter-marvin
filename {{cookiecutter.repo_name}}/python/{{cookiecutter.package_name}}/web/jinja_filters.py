# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
import flask
import jinja2

jinjablue = flask.Blueprint('jinja_filters', __name__)


@jinja2.contextfilter
@jinjablue.app_template_filter()
def split(context, value, delim=None):
    '''Split a string based on a delimiter'''
    if not delim:
        delim = ' '
    return value.split(delim) if value else None

