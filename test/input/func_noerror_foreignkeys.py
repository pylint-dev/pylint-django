"""
Checks that Pylint does not complain about various
methods on Django model fields.
"""
#  pylint: disable=missing-docstring,wrong-import-position
from django.db import models
from django.db.models import ForeignKey, OneToOneField


class Author(models.Model):
    author_name = models.CharField(max_length=100)


class ISBN(models.Model):
    value = models.CharField(max_length=100)


class Book(models.Model):
    book_name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.OneToOneField(ISBN, on_delete=models.CASCADE)

    def get_isbn(self):
        return self.isbn.value

    def get_author_name(self):
        return self.author.author_name


class Fruit(models.Model):
    fruit_name = models.CharField(max_length=20)


class Seed(models.Model):
    fruit = ForeignKey(Fruit, on_delete=models.CASCADE)

    def get_fruit_name(self):
        return self.fruit.fruit_name


class User(models.Model):
    username = models.CharField(max_length=32)


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)

    def get_username(self):
        return self.user.username
