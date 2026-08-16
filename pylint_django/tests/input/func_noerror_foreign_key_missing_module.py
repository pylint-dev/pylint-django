"""
Checks that pylint-django does not crash when resolving string references to missing modules.
"""
# pylint: disable=missing-docstring
from django.db import models


class TestModel(models.Model):
    related = models.ForeignKey("loader.TestRelatedModel", on_delete=models.RESTRICT)
    many = models.ManyToManyField("loader.TestManyModel")
