from django.db.models import fields as django_fields
import datetime
from decimal import Decimal


# --------
# booleans

class BooleanField(bool, django_fields.BooleanField):
    pass


class NullBooleanField(bool, django_fields.NullBooleanField):
    pass


# ------
# strings

class CharField(str, django_fields.CharField):
    pass


class SlugField(CharField, django_fields.SlugField):
    pass


class URLField(CharField, django_fields.URLField):
    pass


class TextField(str, django_fields.TextField):
    pass


class EmailField(CharField, django_fields.EmailField):
    pass


class CommaSeparatedIntegerField(CharField, django_fields.CommaSeparatedIntegerField):
    pass


class FilePathField(CharField, django_fields.FilePathField):
    pass


# -------
# numbers

class IntegerField(int, django_fields.IntegerField):
    pass


class BigIntegerField(IntegerField, django_fields.BigIntegerField):
    pass


class SmallIntegerField(IntegerField, django_fields.SmallIntegerField):
    pass


class PositiveIntegerField(IntegerField, django_fields.PositiveIntegerField):
    pass


class PositiveSmallIntegerField(IntegerField, django_fields.PositiveSmallIntegerField):
    pass


class FloatField(float, django_fields.FloatField):
    pass


class DecimalField(Decimal, django_fields.DecimalField):
    # DecimalField is immutable and does not use __init__, but the Django DecimalField does. To
    # cheat pylint a little bit, we copy the definition of the DecimalField constructor parameters
    # into the __new__ method of Decimal so that Pylint believes we are constructing a Decimal with
    # the signature of DecimalField
    def __new__(cls, verbose_name=None, name=None, max_digits=None, decimal_places=None, **kwargs):
        pass


# --------
# time

class DateField(datetime.date, django_fields.DateField):
    pass


class DateTimeField(datetime.datetime, django_fields.DateTimeField):
    pass


class TimeField(datetime.time, django_fields.TimeField):
    pass


# -------
# misc

class GenericIPAddressField(str, django_fields.GenericIPAddressField):
    pass


class IPAddressField(str, django_fields.IPAddressField):
    pass
