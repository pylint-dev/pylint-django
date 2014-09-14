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


class SlugField(CharField):
    pass


class URLField(CharField):
    pass


class TextField(str, django_fields.TextField):
    pass


class EmailField(CharField):
    pass


class CommaSeparatedIntegerField(CharField):
    pass


class FilePathField(CharField):
    pass


# -------
# numbers

class IntegerField(int, django_fields.IntegerField):
    pass


class BigIntegerField(IntegerField):
    pass


class SmallIntegerField(IntegerField):
    pass


class PositiveIntegerField(IntegerField):
    pass


class PositiveSmallIntegerField(IntegerField):
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
