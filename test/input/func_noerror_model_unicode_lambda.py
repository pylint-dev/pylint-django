"""
Ensures that django models without a __unicode__ method are flagged
"""
#  pylint: disable=C0111,wrong-import-position

from django.db import models


class SomeModel(models.Model):
    something = models.CharField(max_length=255)
    __unicode__ = lambda s: str(s.something)
