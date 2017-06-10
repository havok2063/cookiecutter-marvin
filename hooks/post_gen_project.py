# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
import os
import sys
try:
    import invoke
except ImportError as e:
    invoke = None

"""
    Adds the bin and python directories in your PATH.
"""


def get_paths():
    ''' get the path names '''
    pckg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../{{cookiecutter.repo_name}}')
    repo_name = '{{cookiecutter.repo_name|upper}}_DIR'
    repo_dir = os.path.abspath(pckg_dir)
    os.environ[repo_name] = repo_dir
    bin_path = os.path.join(repo_dir, 'bin')

    # add pythonpath
    python_path = os.path.join(repo_dir, 'python')
    sys.path.insert(0, python_path)
    return repo_dir, bin_path, python_path


@invoke.task
def add_paths(ctx):
    ''' Add bin and python locations to your paths '''

    repo_name = '{{cookiecutter.repo_name|upper}}_DIR'
    repo_dir, bin_path, python_path = get_paths()
    ctx.run('export {0}={1}'.format(repo_name, repo_dir))
    ctx.run('export PATH=$PATH:{0}'.format(bin_path))
    ctx.run('export PYTHONPATH=$PYTHONPATH:{0}'.format(python_path))


if invoke:
    invoke.tasks.Call(add_paths)
else:
    get_paths()

