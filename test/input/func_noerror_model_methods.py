"""
Checks that Pylint does not complain about using Model and Manager methods
"""
#  pylint: disable=C0111,W5101,W5103
from django.db import models


class SomeModel(models.Model):
    pass

if __name__ == '__main__':
    MODEL = SomeModel()
    MODEL.save()
    MODEL.delete()

    COUNT = SomeModel.objects.count()
