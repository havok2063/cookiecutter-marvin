# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#

from __future__ import print_function, division, absolute_import
from setuptools import setup, find_packages

import os
import warnings
from get_version import generate_version_py

from astropy.utils.data import download_file

import argparse
import shutil
import sys


def add_data_file(directory, data_files):
    extern_path = os.path.join(os.path.dirname(__file__), directory)
    for root, __, filenames in os.walk(extern_path):
        for filename in filenames:
            data_files.append(os.path.join('..', root.lstrip('python/'), filename))


def get_data_files(with_web=True):

    data_files = []

    if with_web:
        add_data_file('python/{{cookiecutter.package_name}}/web/configuration/', data_files)
        add_data_file('python/{{cookiecutter.package_name}}/web/lib/', data_files)
        add_data_file('python/{{cookiecutter.package_name}}/web/static/', data_files)
        add_data_file('python/{{cookiecutter.package_name}}/web/templates/', data_files)
        add_data_file('python/{{cookiecutter.package_name}}/web/uwsgi_files/', data_files)

    return data_files


requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
install_requires = [line.strip().replace('==', '>=') for line in open(requirements_file)
                    if not line.strip().startswith('#') and line.strip() != '']

NAME = '{{cookiecutter.package_name}}'
# do not use x.x.x-dev.  things complain.  instead use x.x.xdev
VERSION = '{{cookiecutter.version}}'
RELEASE = 'dev' not in VERSION


def run(data_files, packages):

    setup(name=NAME,
          version=VERSION,
          license='BSD3',
          description='Toolsuite for dealing with the MaNGA dataset',
          long_description=convert_md_to_rst('README.md'),
          author='The Marvin Developers',
          author_email='havok2063@hotmail.com',
          keywords='marvin manga astronomy MaNGA',
          url='https://github.com/sdss/marvin',
          packages=packages,
          package_dir={'': 'python'},
          package_data={'': data_files},
          include_package_data=True,
          install_requires=install_requires,
          scripts=['bin/run_marvin', 'bin/check_marvin'],
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Web Environment',
              'Framework :: Flask',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: BSD License',
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Topic :: Database :: Front-Ends',
              'Topic :: Documentation :: Sphinx',
              'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
              'Topic :: Scientific/Engineering :: Astronomy',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Software Development :: User Interfaces'
          ],
          )


if __name__ == '__main__':

    # Custom parser to decide whether we include or not the web. By default we do.

    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]))

    parser.add_argument('-w', '--noweb', dest='noweb', default=False,
                        action='store_true', help='Does not build the web.')

    # We use parse_known_args because we want to leave the remaining args for distutils
    args = parser.parse_known_args()[0]

    if args.noweb:
        packages = find_packages(where='python', exclude=['{{cookiecutter.package_name}}.web*'])
    else:
        packages = find_packages(where='python')

    data_files = get_data_files(with_web=not args.noweb)

    # Now we remove all our custom arguments to make sure they don't interfere with distutils
    arguments = []
    for action in list(parser._get_optional_actions()):
        if '--help' not in action.option_strings:
            arguments += action.option_strings

    for arg in arguments:
        if arg in sys.argv:
            sys.argv.remove(arg)

    # Runs distutils
    run(data_files, packages)
