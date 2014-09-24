"""
Checks that Pylint does not complain about various
methods on Django model fields.
"""
#  pylint: disable=C0111,W5101
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author)

    def get_author_name(self):
        return self.author.name
