# Check that Meta class definitions for django_tables2 classes
# don't produce old-style-class warnings, see
# https://github.com/PyCQA/pylint-django/issues/56

# pylint: disable=missing-docstring,too-few-public-methods

import django_tables2 as tables
from django.db import models


class SimpleModel(models.Model):
    name = models.CharField()


class SimpleTable(tables.Table):
    class Meta:
        model = SimpleModel
