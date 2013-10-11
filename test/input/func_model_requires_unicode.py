"""
Ensures that django models without a __unicode__ method are flagged
"""
#  pylint: disable=C0111

from django.db import models


class SomeModel(models.Model):
    something = models.CharField(max_length=255)
    # no __unicode__ method

    def lala(self):
        pass
