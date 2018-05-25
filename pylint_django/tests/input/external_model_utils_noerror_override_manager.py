# Check that when overriding the 'objects' attribite of a model class
# with a manager from the django-model-utils package pylint-django
# does not report not-an-iterator error, see
# https://github.com/PyCQA/pylint-django/issues/117
# pylint: disable=missing-docstring, invalid-name

from model_utils.managers import InheritanceManager

from django.db import models


class BaseModel(models.Model):
    name = models.CharField()


class BuggyModel(models.Model):
    objects = InheritanceManager()

    name = models.CharField()


def function():
    for record in BaseModel.objects.all():
        print(record.name)

    for record in BuggyModel.objects.all():
        print(record.name)


class Unit(models.Model):
    sim = models.CharField(max_length=64, null=True, blank=True)
    objects = InheritanceManager()


installed_units = Unit.objects.filter(sim__isnull=False)
ids = [u.sim for u in installed_units]
