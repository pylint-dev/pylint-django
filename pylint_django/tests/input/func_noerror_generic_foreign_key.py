"""
Checks that Pylint does not complain about GenericForeignKey fields:
https://github.com/PyCQA/pylint-django/issues/230
"""
# pylint: disable=missing-docstring

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Ownership(models.Model):
    # for #230 the important bit is this FK field which doesn't
    # have any keyword arguments!
    owner_type = models.ForeignKey(ContentType, models.CASCADE)
    owner_id = models.PositiveIntegerField()
    owner = GenericForeignKey("owner_type", "owner_id")
