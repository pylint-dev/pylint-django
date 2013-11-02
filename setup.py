# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import os
import time


_version = "0.2.dev%s" % int(time.time())
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_short_description = "pylint-django is a Pylint plugin to aid Pylint in recognising and understanding" \
                     "errors caused when using the Django framework"


_transform_dir = 'pylint_django/transforms/transforms'
_package_data = {
    'pylint_django': [
        os.path.join(_transform_dir, name) for name in os.listdir(_transform_dir)
    ]
}


setup(
    name='pylint-django',
    url='https://github.com/landscapeio/pylint-django',
    author='landscape.io',
    author_email='code@landscape.io',
    description=_short_description,
    version=_version,
    packages=_packages,
    package_data=_package_data,
    install_requires=['pylint>=1.0', 'astroid>=1.0', 'pylint-plugin-utils>=0.1'],
    license='GPLv2',
    keywords='pylint django plugin'
)
