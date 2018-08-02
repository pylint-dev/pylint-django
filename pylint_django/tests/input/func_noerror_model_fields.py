"""
Checks that Pylint does not complain about various
methods on Django model fields.
"""
#  pylint: disable=missing-docstring
from __future__ import print_function
from datetime import datetime, date
from decimal import Decimal
from django.db import models


class LotsOfFieldsModel(models.Model):

    bigintegerfield = models.BigIntegerField()
    booleanfield = models.BooleanField(default=True)
    charfield = models.CharField(max_length=40, null=True)
    commaseparatedintegerfield = models.CommaSeparatedIntegerField()
    datetimefield = models.DateTimeField(auto_now_add=True)
    datefield = models.DateField(auto_now_add=True)
    decimalfield = models.DecimalField(max_digits=5, decimal_places=2)
    durationfield = models.DurationField()
    emailfield = models.EmailField()
    filefield = models.FileField(name='test_file', upload_to='test')
    filepathfield = models.FilePathField()
    floatfield = models.FloatField()
    genericipaddressfield = models.GenericIPAddressField()
    imagefield = models.ImageField(name='test_image', upload_to='test')
    ipaddressfield = models.IPAddressField()
    intfield = models.IntegerField(null=True)
    nullbooleanfield = models.NullBooleanField()
    positiveintegerfield = models.PositiveIntegerField()
    positivesmallintegerfield = models.PositiveSmallIntegerField()
    slugfield = models.SlugField()
    smallintegerfield = models.SmallIntegerField()
    textfield = models.TextField()
    timefield = models.TimeField()
    urlfield = models.URLField()

    def __str__(self):
        return self.id

    def boolean_field_tests(self):
        print(self.booleanfield | True)
        print(self.nullbooleanfield | True)

    def string_field_tests(self):
        print(self.charfield.strip())
        print(self.charfield.upper())
        print(self.charfield.replace('x', 'y'))

        print(self.filepathfield.strip())
        print(self.filepathfield.upper())
        print(self.filepathfield.replace('x', 'y'))

        print(self.emailfield.strip())
        print(self.emailfield.upper())
        print(self.emailfield.replace('x', 'y'))

        print(self.textfield.strip())
        print(self.textfield.upper())
        print(self.textfield.replace('x', 'y'))

    def datetimefield_tests(self):
        now = datetime.now()
        print(now - self.datetimefield)
        print(self.datetimefield.ctime())

    def datefield_tests(self):
        now = date.today()
        print(now - self.datefield)
        print(self.datefield.isoformat())

    def decimalfield_tests(self):
        print(self.decimalfield.compare(Decimal('1.4')))

    def durationfield_tests(self):
        now = datetime.now()
        print(now - self.durationfield)
        print(self.durationfield.total_seconds())

    def filefield_tests(self):
        self.filefield.save('/dev/null', 'TEST')
        print(self.filefield.file)
        self.imagefield.save('/dev/null', 'TEST')
        print(self.imagefield.file)

    def numberfield_tests(self):
        print(self.intfield + 5)
        print(self.bigintegerfield + 4)
        print(self.smallintegerfield + 3)
        print(self.positiveintegerfield + 2)
        print(self.positivesmallintegerfield + 1)
