"""
Checks that Pylint does not complain about various
methods on Django form forms.
"""
#  pylint: disable=missing-docstring
from __future__ import print_function

from datetime import date, datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm


class ManyFieldsForm(forms.Form):

    booleanfield = forms.BooleanField()
    charfield = forms.CharField(max_length=40, null=True)
    datetimefield = forms.DateTimeField(auto_now_add=True)
    datefield = forms.DateField(auto_now_add=True)
    decimalfield = forms.DecimalField(max_digits=5, decimal_places=2)
    durationfield = forms.DurationField()
    emailfield = forms.EmailField()
    filefield = forms.FileField(name="test_file", upload_to="test")
    filepathfield = forms.FilePathField(path="/some/path")
    floatfield = forms.FloatField()
    genericipaddressfield = forms.GenericIPAddressField()
    imagefield = forms.ImageField(name="test_image", upload_to="test")
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
        print(self.charfield.replace("x", "y"))

        print(self.filepathfield.strip())
        print(self.filepathfield.upper())
        print(self.filepathfield.replace("x", "y"))

        print(self.emailfield.strip())
        print(self.emailfield.upper())
        print(self.emailfield.replace("x", "y"))

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

    def durationfield_tests(self):
        now = datetime.now()
        print(now - self.durationfield)
        print(self.durationfield.total_seconds())

    def filefield_tests(self):
        print(self.filefield)
        print(self.imagefield)

    def numberfield_tests(self):
        print(self.intfield + 5)


_ = UserCreationForm.declared_fields
