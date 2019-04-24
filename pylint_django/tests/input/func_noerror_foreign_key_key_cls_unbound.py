"""
Checks that Pylint does not complain about ForeignKey pointing to model
in module of models package
"""
# pylint: disable=missing-docstring
from django.db import models


class FairyTail(models.Model):
    # fails with "UnboundLocalError: local variable 'key_cls' referenced before assignment"
    author = models.ForeignKey(to='input.Author', null=True, on_delete=models.CASCADE)

    def get_author_name(self):
        return self.author.id
