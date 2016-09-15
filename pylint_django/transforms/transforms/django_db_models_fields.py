from django.db.models import fields as django_fields
import datetime
from decimal import Decimal
from uuid import UUID


# --------
# booleans
from utils import PY3


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
# date/time

# In Python3, the date and datetime objects are immutable, so we need to do
# the same __new__ / __init__ fiddle as for Decimal

class DateField(datetime.date, django_fields.DateField):
    if PY3:
        def __new__(cls, verbose_name=None, name=None, auto_now=False,
                    auto_now_add=False, **kwargs):
            pass


class DateTimeField(datetime.datetime, django_fields.DateTimeField):
    if PY3:
        def __new__(cls, verbose_name=None, name=None, auto_now=False,
                    auto_now_add=False, **kwargs):
            pass


class TimeField(datetime.time, django_fields.TimeField):
    if PY3:
        def __new__(cls, verbose_name=None, name=None, auto_now=False,
                    auto_now_add=False, **kwargs):
            pass


class DurationField(datetime.timedelta, django_fields.DurationField):
    if PY3:
        def __new__(cls, verbose_name=None, name=None, **kwargs):
            pass


# -------
# misc

class GenericIPAddressField(str, django_fields.GenericIPAddressField):
    pass


class IPAddressField(str, django_fields.IPAddressField):
    pass


class UUIDField(UUID, django_fields.UUIDField):
    pass
