"""
Checks that Pylint does not complain about using Model and Manager methods
"""
#  pylint: disable=missing-docstring
from django.db import models


class SomeModel(models.Model):
    pass

if __name__ == '__main__':
    MODEL = SomeModel()
    MODEL.save()
    MODEL.delete()

    COUNT = SomeModel.objects.count()
    # added in django 1.6
    FIRST = SomeModel.objects.first()
    LAST = SomeModel.objects.last()
