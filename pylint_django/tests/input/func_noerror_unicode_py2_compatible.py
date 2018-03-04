"""
Ensures that no '__unicode__ missing' warning is emitted if the
Django python3/2 compatability dectorator is used

See https://github.com/PyCQA/pylint-django/issues/10
"""
#  pylint: disable=missing-docstring
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


@python_2_unicode_compatible
class ModelName(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
