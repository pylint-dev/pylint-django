"""
Ensures that django models without a __unicode__ method are flagged,
but only models which are not abstract
"""
#  pylint: disable=C0111

from django.db import models


class SomeModel(models.Model):
    something = models.CharField(max_length=255)
    # no __unicode__ method

    something.something_else = 1

    def lala(self):
        pass


class SomeAbstractModel(models.Model):
    class Meta:
        abstract = True
