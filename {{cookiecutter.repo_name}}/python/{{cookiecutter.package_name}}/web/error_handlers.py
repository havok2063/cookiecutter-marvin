# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from flask import request, current_app as app
from flask import Blueprint, jsonify, render_template, g

errors = Blueprint('web_error_handlers', __name__)


def make_error_json(error, name, code):
    ''' creates the error json dictionary for API errors '''
    shortname = name.lower().replace(' ', '_')
    messages = {'error': shortname,
                'message': error.description if hasattr(error, 'description') else None,
                'status_code': code}
    return jsonify({'api_error': messages}), code


def make_error_page(app, name, code, sentry=None, data=None):
    ''' creates the error page dictionary for web errors '''
    shortname = name.lower().replace(' ', '_')
    error = {}
    error['title'] = '{{cookiecutte.package_title}} | {0}'.format(name)
    error['page'] = request.url
    error['event_id'] = g.get('sentry_event_id', None)
    error['data'] = data
    if sentry:
        error['public_dsn'] = sentry.client.get_public_dsn('https')
    app.logger.error('{0} Exception {1}'.format(name, error))
    return render_template('errors/{0}.html'.format(shortname), **error), code


# ----------------
# Error Handling
# ----------------

def _is_api(request):
    ''' Checks if the error comes from the api '''
    return request.blueprint == 'api' or 'api' in request.url


@errors.errorhandler(404)
def page_not_found(error):
    name = 'Page Not Found'
    if _is_api(request):
        return make_error_json(error, name, 404)
    else:
        return make_error_page(app, name, 404)

