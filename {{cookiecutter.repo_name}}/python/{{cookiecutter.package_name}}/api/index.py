# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from {{cookiecutter.package_name}}.api.base import BaseView
from flask import jsonify


class MainView(BaseView):
    ''' Class describing API calls related to MaNGA Cubes '''

    route_base = '/'

    def index(self):
        '''Returns general info

        .. :quickref: Main; Get main info

        :query string release: the release of MaNGA
        :resjson int status: status of response. 1 if good, -1 if bad.
        :resjson string error: error message, null if None
        :resjson json inconfig: json of incoming configuration, if any
        :resjson string traceback: traceback of an error, null if None
        :resjson string data: data message
        :resheader Content-Type: application/json
        :statuscode 200: no error
        :statuscode 422: invalid input parameters

        **Example request**:

        .. sourcecode:: http

           GET /{{cookiecutter.package_name}}/api/ HTTP/1.1
           Host: localhost:8080
           Accept: application/json, */*

        **Example response**:

        .. sourcecode:: http

           HTTP/1.1 200 OK
           Content-Type: application/json
           {
              "status": 1,
              "error": null,
              "inconfig": {},
              "traceback": null,
              "data": "this is a data from an API response!"
           }

        '''
        #args = av.manual_parse(self, request)
        self.results['status'] = 1
        self.results['data'] = 'this is data from an API response!'
        return jsonify(self.results)

