# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-08-12 15:35:41
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-08-12 15:36:16

from __future__ import print_function, division, absolute_import
import os
from invoke import Collection, task


@task
def clean_docs(ctx):
    ''' Cleans up the docs '''
    print('Cleaning the docs')
    ctx.run("rm -rf docs/sphinx/_build")


@task(clean_docs)
def build_docs(ctx):
    ''' Builds the Sphinx docs '''
    print('Building the Sphinx docs')
    os.chdir('docs/sphinx')
    ctx.run("make html")


@task
def clean(ctx):
    ''' Cleans up the crap '''
    print('Cleaning')
    # ctx.run("rm -rf docs/sphinx/_build")
    ctx.run("rm -rf htmlcov")
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")


@task(clean)
def deploy(ctx):
    ''' Deploy to pypi '''
    print('Deploying to Pypi!')
    ctx.run("python setup.py sdist bdist_wheel --universal")
    ctx.run("twine upload dist/*")


ns = Collection(clean, deploy)
docs = Collection('docs')
docs.add_task(build_docs, 'build')
docs.add_task(clean_docs, 'clean')
ns.add_collection(docs)
