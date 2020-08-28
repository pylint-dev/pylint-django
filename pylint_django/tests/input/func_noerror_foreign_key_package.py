"""
Checks that Pylint does not complain about ForeignKey pointing to model
in module of models package
"""
# pylint: disable=model-no-explicit-str,model-no-explicit-str,missing-docstring
from django.db import models


class Book(models.Model):
    author = models.ForeignKey(to='pylint_django.tests.input.Author', on_delete=models.CASCADE)

    def get_author_name(self):
        return self.author.id
