#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup
here = os.path.abspath(os.path.dirname(__file__))

NAME = 'canif'
DESCRIPTION = 'INSEE management scripts.'
VERSION = "0.1-dev"
README = open(os.path.join(here, 'README.rst')).read()
AUTHOR = u'Rémy Hubscher'
EMAIL = u'hubscher.remy@gmail.com'
URL = 'https://github.com/Natim/{name}'.format(name=NAME)
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'License :: OSI Approved :: BSD License',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 2.6',
               'Topic :: Internet :: WWW/HTTP',
               'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
               'Framework :: Pyramid']
KEYWORDS = ['Canif']
PACKAGES = [NAME.replace('-', '_')]
REQUIREMENTS = [
    'setuptools',
    'six',
    'hiredis',
    'redis'
]
DEPENDENCY_LINKS = []
ENTRY_POINTS = {
    'console_scripts': [
        'import_insee_variables = canif:import_insee_variables',
        'import_insee_data = canif:import_insee_data',
        'export_insee = canif:export_insee',
        'canif_serve = canif.server:serve',
    ]}

if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=README,
          classifiers=CLASSIFIERS,
          keywords=' '.join(KEYWORDS),
          author=AUTHOR,
          author_email=EMAIL,
          url=URL,
          license='BSD',
          packages=PACKAGES,
          include_package_data=True,
          zip_safe=False,
          install_requires=REQUIREMENTS,
          dependency_links=DEPENDENCY_LINKS,
          entry_points=ENTRY_POINTS)
