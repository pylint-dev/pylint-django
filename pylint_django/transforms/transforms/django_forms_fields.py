import datetime
from decimal import Decimal
from django.forms import fields as django_fields


# --------
# booleans

class BooleanField(bool, django_fields.BooleanField):
    pass


class NullBooleanField(bool, django_fields.NullBooleanField):
    pass


# -------
# strings

class CharField(str, django_fields.CharField):
    pass


class EmailField(CharField, django_fields.EmailField):
    pass


class GenericIPAddressField(CharField, django_fields.GenericIPAddressField):
    pass


class IPAddressField(CharField, django_fields.IPAddressField):
    pass


class SlugField(CharField, django_fields.SlugField):
    pass


class URLField(CharField, django_fields.URLField):
    pass


class RegexField(CharField, django_fields.RegexField):
    pass


class FilePathField(CharField, django_fields.FilePathField):
    pass


# -------
# numbers

class IntegerField(int, django_fields.IntegerField):
    pass


class DecimalField(Decimal, django_fields.DecimalField):
    # DecimalField is immutable and does not use __init__, but the Django DecimalField does. To
    # cheat pylint a little bit, we copy the definition of the DecimalField constructor parameters
    # into the __new__ method of Decimal so that Pylint believes we are constructing a Decimal with
    # the signature of DecimalField
    def __new__(cls, max_value=None, min_value=None, max_digits=None, decimal_places=None, *args, **kwargs):
        pass


class FloatField(float, django_fields.FloatField):
    pass


# -------
# date/time

class DateField(datetime.date, django_fields.DateField):
    pass


class DateTimeField(datetime.datetime, django_fields.DateTimeField):
    pass


class SplitDateTimeField(datetime.datetime, django_fields.SplitDateTimeField):
    pass


class TimeField(datetime.time, django_fields.TimeField):
    pass


# --------
# choice

class ChoiceField(object, django_fields.ChoiceField):
    pass


class MultipleChoiceField(ChoiceField, django_fields.MultipleChoiceField):
    pass


class TypedChoiceField(ChoiceField, django_fields.TypedChoiceField):
    pass


class TypedMultipleChoiceField(ChoiceField, django_fields.TypedMultipleChoiceField):
    pass
