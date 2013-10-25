# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import time


_version = "0.1.dev%s" % int(time.time())
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_short_description = "pylint-django is a Pylint plugin to aid Pylint in recognising and understanding" \
                     "errors caused when using the Django framework"


setup(
    name='pylint-django',
    url='https://github.com/landscapeio/pylint-django',
    author='landscape.io',
    author_email='code@landscape.io',
    description=_short_description,
    version=_version,
    packages=_packages,
    install_requires=['pylint', 'astroid', 'pylint-plugin-utils'],
    license='GPLv2',
    keywords='pylint django plugin'
)
