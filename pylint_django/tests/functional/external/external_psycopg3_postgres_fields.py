"""
Checks that Pylint does not complain Postgres model fields.
"""
#  pylint: disable=C0111,W5101
from __future__ import print_function

from django.contrib.postgres import fields
from django.db import models


class PostgresFieldsModel(models.Model):
    period = fields.DateRangeField(null=False, blank=False)

    def rangefield_tests(self):
        print(self.period.lower)
        print(self.period.upper)
