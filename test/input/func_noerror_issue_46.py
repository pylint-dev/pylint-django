"""
Checks that Pylint does not complain about raising DoesNotExist
"""
#  pylint: disable=C0111
from django.db import models


class SomeModel(models.Model):
    pass

raise SomeModel.DoesNotExist
