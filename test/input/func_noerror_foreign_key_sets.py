"""
Checks that Pylint does not complain about foreign key sets on models
"""
#  pylint: disable=C0111,R0903,W0232
__revision__ = ''

from django.db import models


class SomeModel(models.Model):
    name = models.CharField(max_length=20)

    def get_others(self):
        return self.othermodel_set.all()


class OtherModel(models.Model):
    count = models.IntegerField()
    something = models.ForeignKey(SomeModel)
