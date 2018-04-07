"""
Test to validate that pylint_django doesn't produce
Instance of 'SubFactory' has no 'pk' member (no-member) warnings
"""
# pylint: disable=attribute-defined-outside-init, missing-docstring, too-few-public-methods
import factory

from django import test
from django.db import models


class Author(models.Model):
    name = models.CharField()


class Book(models.Model):
    title = models.CharField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'Author'

    name = factory.Sequence(lambda n: 'Author %d' % n)


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'Book'

    title = factory.Sequence(lambda n: 'Book %d' % n)
    author = factory.SubFactory(AuthorFactory)


class BookTestCase(test.LiveServerTestCase):
    serialized_rollback = True

    def _fixture_setup(self):
        super(BookTestCase, self)._fixture_setup()
        self.book = BookFactory()

    def test_author_is_not_none(self):
        self.assertGreater(self.book.pk, 0)
        self.assertGreater(self.book.author.pk, 0)

        self.assertIsNotNone(self.book.title)
        self.assertIsNotNone(self.book.author.name)
