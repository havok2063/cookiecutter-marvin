# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from flask_classful import FlaskView
from flask import request


class BaseWebView(FlaskView):
    ''' This is the Base Web View for all pages '''

    def __init__(self, page):
        self.base = {}
        self.base['intro'] = 'Welcome to {{cookiecutter.package_title}}!'
        self.update_title(page)
        self._endpoint = self._release = None
        self._drpver = self._dapver = None

    def before_request(self, *args, **kwargs):
        ''' this runs before every single request '''
        self.base['error'] = None
        self._endpoint = request.endpoint

    def after_request(self, name, response):
        ''' this runs after every single request '''
        return response

    def update_title(self, page):
        ''' Update the title and page '''
        self.base['title'] = page.title().split('-')[0] if 'main' in page \
            else page.title().replace('-', ' | ')
        self.base['page'] = page

    def reset_dict(self, mydict, exclude=None):
        ''' resets the page dictionary '''
        mydict['error'] = self.base['error']
        exclude = exclude if isinstance(exclude, list) else [exclude]
        diffkeys = set(mydict) - set(self.base)
        for key, val in mydict.items():
            if key in diffkeys and (key not in exclude):
                mydict[key] = '' if isinstance(val, str) else None
