from django.contrib.postgres import fields as django_fields
from psycopg2 import extras


# --------
# lists

class ArrayField(list, django_fields.ArrayField):
    pass


# --------
# dicts

class HStoreField(dict, django_fields.HStoreField):
    pass


class JSONField(dict, django_fields.JSONField):
    pass


# --------
# ranges

class RangeField(extras.Range, django_fields.RangeField):
    pass


class IntegerRangeField(extras.NumericRange, django_fields.IntegerRangeField):
    pass


class BigIntegerRangeField(extras.NumericRange, django_fields.BigIntegerRangeField):
    pass


class FloatRangeField(extras.NumericRange, django_fields.FloatRangeField):
    pass


class DateTimeRangeField(extras.DateTimeTZRange, django_fields.DateRangeField):
    pass


class DateRangeField(extras.DateRange, django_fields.DateRangeField):
    pass
