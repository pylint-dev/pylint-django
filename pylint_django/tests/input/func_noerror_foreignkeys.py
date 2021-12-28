"""
Checks that Pylint does not complain about various
methods on Django model fields.
"""
#  pylint: disable=missing-docstring,wrong-import-position
from django.db import models
from django.db.models import ForeignKey, OneToOneField


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Author(models.Model):
    author_name = models.CharField(max_length=100)


class ISBN(models.Model):
    value = models.CharField(max_length=100)


class Book(models.Model):
    book_name = models.CharField(max_length=100)
    # Check this works with and without `to` keyword
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE)
    isbn = models.OneToOneField(to=ISBN, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def get_isbn(self):
        return self.isbn.value

    def get_author_name(self):
        return self.author.author_name


class Fruit(models.Model):
    fruit_name = models.CharField(max_length=20)


class Seed(models.Model):
    fruit = ForeignKey(to=Fruit, on_delete=models.CASCADE)

    def get_fruit_name(self):
        return self.fruit.fruit_name


class User(models.Model):
    username = models.CharField(max_length=32)


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)

    def get_username(self):
        return self.user.username


class Human(models.Model):
    child = ForeignKey("self", on_delete=models.SET_NULL, null=True)
    parent = ForeignKey(to="self", on_delete=models.SET_NULL, null=True)

    def get_grandchild(self):
        return self.child.child

    def get_grandparent(self):
        return self.parent.parent


class UserPreferences(models.Model):
    """
    Used for testing FK which refers to another model by
    string, not model class, see
    https://github.com/PyCQA/pylint-django/issues/35
    """

    user = ForeignKey("User", on_delete=models.CASCADE)


class UserAddress(models.Model):
    user = OneToOneField(to="User", on_delete=models.CASCADE)
    line_1 = models.CharField(max_length=100)
    line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
