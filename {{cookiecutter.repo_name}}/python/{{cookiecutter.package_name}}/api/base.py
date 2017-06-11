# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division
from flask_classful import FlaskView
from flask import request
from {{cookiecutter.package_name}}.api import process_request


class BaseView(FlaskView):
    '''Super Class for all API Views to handle all global API items of interest'''

    def __init__(self):
        self.reset_results()
        #bconfig.mode = 'local'

    def reset_results(self):
        self.results = {'data': None, 'status': -1, 'error': None, 'traceback': None}

    def update_results(self, newresults):
        self.results.update(newresults)

    def reset_status(self):
        self.results['status'] = -1

    def add_config(self):
        pass

    # def add_config(self):
    #     utahconfig = {'utahconfig': {'mode': config.mode, 'release': config.release}}
    #     self.update_results(utahconfig)

    def _pop_args(self, kwargs, arglist=None):
        if arglist:
            arglist = [arglist] if not isinstance(arglist, (list, tuple)) else arglist

            for item in arglist:
                tmp = kwargs.pop(item, None)

        return kwargs

    def before_request(self, *args, **kwargs):
        form = process_request(request=request)
        self._release = form.get('release', None) if form else None
        self._endpoint = request.endpoint
        self.results['inconfig'] = form
        if form:
            for key, val in form.items():
                bconfig.__setattr__(key, val)
        # adds the out going config info into the results (placed here since didn't work in
        # after_request; obstensibly the in and out configs should match)
        self.add_config()

    def after_request(self, name, response):
        """This performs a reset of the results dict after every request method runs.
        See Flask-Classful for more info on after_request."""

        self.reset_results()
        return response






