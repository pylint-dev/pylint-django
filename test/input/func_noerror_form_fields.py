"""
Checks that Pylint does not complain about various
methods on Django form forms.
"""
#  pylint: disable=C0111,R0904
from __future__ import print_function
from datetime import datetime, date
from django import forms


class ManyFieldsForm(forms.Form):

    booleanfield = forms.BooleanField(default=True)
    charfield = forms.CharField(max_length=40, null=True)
    datetimefield = forms.DateTimeField(auto_now_add=True)
    datefield = forms.DateField(auto_now_add=True)
    decimalfield = forms.DecimalField(max_digits=5, decimal_places=2)
    emailfield = forms.EmailField()
    filepathfield = forms.FilePathField()
    floatfield = forms.FloatField()
    genericipaddressfield = forms.GenericIPAddressField()
    ipaddressfield = forms.IPAddressField()
    intfield = forms.IntegerField(null=True)
    nullbooleanfield = forms.NullBooleanField()
    slugfield = forms.SlugField()
    timefield = forms.TimeField()
    urlfield = forms.URLField()

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

    def datetimefield_tests(self):
        now = datetime.now()
        print(now - self.datetimefield)
        print(self.datetimefield.ctime())

    def datefield_tests(self):
        now = date.today()
        print(now - self.datefield)
        print(self.datefield.isoformat())

    def decimalfield_tests(self):
        print(self.decimalfield.adjusted())

    def numberfield_tests(self):
        print(self.intfield + 5)
