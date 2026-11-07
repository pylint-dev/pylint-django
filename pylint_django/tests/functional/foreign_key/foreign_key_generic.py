"""
Checks that Pylint does not complain about GenericForeignKey fields:
https://github.com/pylint-dev/pylint-django/issues/230
https://github.com/pylint-dev/pylint-django/issues/496
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

    # for #496 the related object can be an instance of any model,
    # so accessing its attributes must not raise no-member
    @property
    def owner_guid(self):
        return self.owner.guid if self.owner else None

    def owner_name(self):
        return self.owner.get_name()
