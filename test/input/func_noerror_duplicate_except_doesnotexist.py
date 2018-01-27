"""
Checks that Pylint does not complain about duplicate
except blocks catching DoesNotExist exceptions:
https://github.com/PyCQA/pylint-django/issues/81
"""
#  pylint: disable=missing-docstring
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)


class Author(models.Model):
    name = models.CharField(max_length=100)

def dummy_func():
    try:
        print("foo")
    except Book.DoesNotExist:
        print("bar")
    except Author.DoesNotExist:
        print("baz")
