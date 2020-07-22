"""
Checks that PyLint correctly handles string foreign keys
https://github.com/PyCQA/pylint-django/issues/243
"""
# pylint: disable=missing-docstring, hard-coded-auth-user
from django.db import models


class Book(models.Model):
    author = models.ForeignKey("test_app.Author", models.CASCADE)
    user = models.ForeignKey("auth.User", models.PROTECT)
