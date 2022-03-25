#!/bin/bash
pylint --rcfile=tox.ini --load-plugins=pylint_django setup.py | grep django-not-configured
