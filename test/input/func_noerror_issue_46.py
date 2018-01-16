"""
Checks that Pylint does not complain about raising DoesNotExist
"""
#  pylint: disable=missing-docstring
from django.db import models


class SomeModel(models.Model):
    pass

raise SomeModel.DoesNotExist
