"""
Tests to make sure that access to _meta on a model does not raise
a protected-access warning, as it is part of the public API since
Django 1.8
(see https://github.com/PyCQA/pylint-django/issues/66,
and https://docs.djangoproject.com/en/1.9/ref/models/meta/)
"""
#  pylint: disable=missing-docstring
from __future__ import print_function

from django.db import models


class ModelWhichLikesMeta(models.Model):
    ursuary = models.BooleanField(default=False)

    def do_a_thing(self):
        return self._meta.get_field("ursuary")


if __name__ == "__main__":
    MODEL = ModelWhichLikesMeta()
    MODEL.save()
    print(MODEL._meta.get_field("ursuary"))
    print(MODEL.do_a_thing())
