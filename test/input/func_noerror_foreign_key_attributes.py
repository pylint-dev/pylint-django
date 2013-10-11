"""
Checks that Pylint does not complain about foreign key sets on models
"""
#  pylint: disable=C0111,W5101

from django.db import models


class SomeModel(models.Model):
    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField()


class OtherModel(models.Model):
    something = models.ForeignKey(SomeModel)

    def something_doer(self):
        return '%s - %s' % (self.something.name, self.something.timestamp)
