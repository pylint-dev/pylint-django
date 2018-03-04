"""
Checks that Pylint does not complain about various
methods on many-to-many relationships
"""
#  pylint: disable=missing-docstring
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    good = models.BooleanField(default=False)


class Author(models.Model):
    name = models.CharField(max_length=100)
    wrote = models.ManyToManyField(Book, verbose_name="Book",
                                   related_name='books')

    def get_good_books(self):
        return self.wrote.filter(good=True)

    def is_author_of(self, book):
        return book in list(self.wrote.all())

    def wrote_how_many(self):
        return self.wrote.count()
