"""
Checks that Pylint does not complain Postgres model fields.
"""
#  pylint: disable=C0111,W5101
from __future__ import print_function

from django.contrib.postgres import fields
from django.db import models


class PostgresFieldsModel(models.Model):
    arrayfield = fields.ArrayField(models.CharField())
    hstorefield = fields.HStoreField()
    jsonfield = fields.JSONField()
    rangefield = fields.RangeField()
    integerrangefield = fields.IntegerRangeField()
    bigintegerrangefield = fields.BigIntegerRangeField()
    floatrangefield = fields.FloatRangeField()
    datetimerangefield = fields.DateTimeRangeField()
    daterangefield = fields.DateRangeField()

    def arrayfield_tests(self):
        sorted_array = self.arrayfield.sort()
        print(sorted_array)

    def dictfield_tests(self):
        print(self.hstorefield.keys())
        print(self.hstorefield.values())
        print(self.hstorefield.update({'foo': 'bar'}))

        print(self.jsonfield.keys())
        print(self.jsonfield.values())
        print(self.jsonfield.update({'foo': 'bar'}))

    def rangefield_tests(self):
        print(self.rangefield.lower)
        print(self.rangefield.upper)

        print(self.integerrangefield.lower)
        print(self.integerrangefield.upper)

        print(self.bigintegerrangefield.lower)
        print(self.bigintegerrangefield.upper)

        print(self.floatrangefield.lower)
        print(self.floatrangefield.upper)

        print(self.datetimerangefield.lower)
        print(self.datetimerangefield.upper)

        print(self.daterangefield.lower)
        print(self.daterangefield.upper)
