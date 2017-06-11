# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from flask import current_app, Blueprint, render_template, jsonify
from flask import session as current_session, request, redirect, url_for
from flask_classful import route
from {{cookiecutter.package_name}}.web.controllers import BaseWebView


index = Blueprint("index", __name__)


class {{cookiecutter.package_title}}(BaseWebView):
    route_base = '/'

    def __init__(self):
        super({{cookiecutter.package_title}}, self).__init__('{{cookiecutter.package_name}}-main')
        self.main = self.base.copy()

    def before_request(self, *args, **kwargs):
        super({{cookiecutter.package_title}}, self).before_request(*args, **kwargs)
        self.reset_dict(self.main)

    @route('/', endpoint='home')
    def index(self):
        current_app.logger.info('Welcome to {{cookiecutter.package_title}} Web!')

        return render_template("index.html", **self.main)

    def status(self):
        return 'OK'

{{cookiecutter.package_title}}.register(index)
