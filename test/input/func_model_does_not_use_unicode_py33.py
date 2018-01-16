"""
Ensures that django models without a __unicode__ method are flagged
"""
#  pylint: disable=missing-docstring

from django.db import models


class SomeModel(models.Model):
    something = models.CharField(max_length=255)
    # no __unicode__ method

    something.something_else = 1

    def lala(self):
        pass

    def __unicode__(self):
        return self.something
