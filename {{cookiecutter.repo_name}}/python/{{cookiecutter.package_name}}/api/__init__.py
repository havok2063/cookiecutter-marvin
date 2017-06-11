# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from flask import request


def processRequest(request=None, as_dict=None, param=None):
    '''Generally process the request for POST or GET, and build a form dictionary

        Parameters:
            request (request):
                HTTP request object containing POST or GET data
            as_dict (bool):
                Boolean indicating whether to return the data as a standard dict or not
            param (str):
                Parameter name to extract from the request form
        Returns:
            Dict or ImmutableMultiDict
    '''

    # get form data
    if request.method == 'POST':
        if not request.form:
            # if data is content-type json
            data = request.get_json()
        else:
            # if data is content-type form
            data = request.form
    elif request.method == 'GET':
        data = request.args
    else:
        return {}

    # # if no data at all, return nothing
    if param and data:
        return data.get(param, None)

    # convert ImmutableMultiDict to dictionary (if get or post-form) or use dict if post-json
    if as_dict:
        if isinstance(data, dict):
            form = data
        else:
            # use multidict lists and iterlists to group multiple values for same in key into list
            try:
                # py2.7
                form = {key: val if len(val) > 1 else val[0] for key, val in data.iterlists()}
            except AttributeError:
                # py3.5
                form = {key: val if len(val) > 1 else val[0] for key, val in data.lists()}
    else:
        form = data

    return form
