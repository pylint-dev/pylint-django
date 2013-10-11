"""
This test ensures that a 'Meta' class defined on a Django model does
not raise warnings such as 'old-style-class' and 'too-few-public-methods'
"""
#  pylint: disable=C0111,W5101

from django.db import models


class SomeModel(models.Model):
    class Meta:
        ordering = ('-id',)
