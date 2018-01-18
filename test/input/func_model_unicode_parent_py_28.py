"""
Ensures that django models whose parent have a
__unicide__ method are not flagged
"""
#  pylint: disable=missing-docstring
from django.db import models


class MyModel(models.Model):
    def __unicode__(self):
        return str(self.id)


class MySubclassModel(MyModel):
    pass
