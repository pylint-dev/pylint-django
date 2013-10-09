"""
Checks that Pylint does not complain about foreign key sets on models
"""
#  pylint: disable=C0111,R0903,W0232
__revision__ = ''

from django.db import models


class SomeModel(models.Model):
    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField()


class OtherModel(models.Model):
    something = models.ForeignKey(SomeModel)

    def something_doer(self):
        return '%s - %s' % (self.something.name, self.something.timestamp)
