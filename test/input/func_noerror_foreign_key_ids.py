"""
Checks that Pylint does not complain about foreign key id access
"""
#  pylint: disable=C0111,W5101,wrong-import-position
from django.db import models


class SomeModel(models.Model):
    count = models.IntegerField()


class SomeOtherModel(models.Model):
    some_model = models.ForeignKey(SomeModel)
    number = models.IntegerField()

    def do_something(self):
        self.number = self.some_model_id
