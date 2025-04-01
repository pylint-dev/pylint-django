#!/bin/bash
pylint --rcfile=tox.ini --load-plugins=pylint_django pylint_django/ | grep django-not-available
