# -*- coding: UTF-8 -*-
"""
Setup module for Pylint plugin for Django.
"""
import os
from setuptools import setup, find_packages

VERSION = '0.9.1'
PACKAGES = find_packages(exclude=[
    '*.tests',
    '*.tests.*',
    'tests.*',
    'tests',
])

SHORT_DESCRIPTION = 'A Pylint plugin to help Pylint understand the Django web framework'

TRANSFORM_DIR = 'pylint_django/transforms/transforms'
PACKAGE_DATA = {
    'pylint_django': [
        os.path.join('transforms/transforms', name) for name in os.listdir(TRANSFORM_DIR)
    ]
}

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Topic :: Software Development :: Quality Assurance',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
)

INSTALL_REQUIRES = [
    'pylint-plugin-utils>=0.2.1',
    'pylint>=1.8.2',
]


setup(
    name='pylint-django',
    url='https://github.com/PyCQA/pylint-django',
    author='landscape.io',
    author_email='code@landscape.io',
    description=SHORT_DESCRIPTION,
    version=VERSION,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    license='GPLv2',
    classifiers=CLASSIFIERS,
    keywords=['pylint', 'django', 'plugin'],
    zip_safe=False,
)
