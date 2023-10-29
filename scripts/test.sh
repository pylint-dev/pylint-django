#!/bin/bash
# TODO: The following code duplicates requirements from pyproject.toml for test dependencies. This is because during
#  the CI run, tox builds a package using the pyproject.toml and installs it; this means that it does not install
#  dev-dependencies including the ones needed for tests to pass. Frustratingly, the "install extras" feature of
#  tox does not appear to work to solve this by putting the test deps into an optional grouping. For now, this
#  hardcoded list will have to do in order to fix the CI... see #376
pip install pytest pytest-cov \
  "django-tables2>=2.6.0" \
  "factory-boy>=3.3.0" \
  "django-tastypie>=0.14.6" \
  "djangorestframework>=3.13.1"

python pylint_django/tests/test_func.py -v "$@"
