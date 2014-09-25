# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import os


_version = '0.5.3'
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_short_description = "pylint-django is a Pylint plugin to aid Pylint in recognising and understanding" \
                     "errors caused when using the Django framework"


_transform_dir = 'pylint_django/transforms/transforms'
_package_data = {
    'pylint_django': [
        os.path.join('transforms/transforms', name) for name in os.listdir(_transform_dir)
    ]
}

_classifiers = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Topic :: Software Development :: Quality Assurance',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
)

_install_requires=[
    'pylint>=1.0', 
    'astroid>=1.0', 
    'logilab-common>=0.60.0', 
    'pylint-plugin-utils>=0.2.1'
]

setup(
    name='pylint-django',
    url='https://github.com/landscapeio/pylint-django',
    author='landscape.io',
    author_email='code@landscape.io',
    description=_short_description,
    version=_version,
    packages=_packages,
    package_data=_package_data,
    install_requires=_install_requires,
    license='GPLv2',
    classifiers=_classifiers,
    keywords='pylint django plugin'
)
