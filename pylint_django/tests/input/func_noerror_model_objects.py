# Test that defining `objects` as a regular model manager
# doesn't raise issues, see
# https://github.com/PyCQA/pylint-django/issues/144
#
# pylint: disable=missing-docstring

from django.db import models


class ModelWithRegularManager(models.Model):
    objects = models.Manager()

    name = models.CharField()


def function():
    record = ModelWithRegularManager.objects.all()[0]

    for record in ModelWithRegularManager.objects.all():
        print(record.name)
