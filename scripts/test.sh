#!/bin/bash
# TODO : find out why tox refuses to install this or install any dev dependencies from poetry :-|
pip install 'pytest>=7.3.1'

python pylint_django/tests/test_func.py -v "$@"
