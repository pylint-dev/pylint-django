"""
Standard WSGI config created by django-admin startproject.

Used to verify pylint_django doesn't produce invalid-name for
the application variable. See:
https://github.com/PyCQA/pylint-django/issues/77
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproj.settings")

application = get_wsgi_application()
