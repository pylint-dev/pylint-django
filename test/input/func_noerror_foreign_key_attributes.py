"""
Checks that Pylint does not complain about foreign key sets on models
"""
#  pylint: disable=missing-docstring

from django.db import models


class SomeModel(models.Model):
    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField()


class OtherModel(models.Model):
    something = models.ForeignKey(SomeModel, on_delete=models.CASCADE)
    elsething = models.OneToOneField(SomeModel, on_delete=models.CASCADE)

    def something_doer(self):
        part_a = '%s - %s' % (self.something.name, self.something.timestamp)
        part_b = self.elsething.name
        return part_a, part_b
