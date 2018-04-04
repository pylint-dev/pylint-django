"""
Ensures that django models with a __str__ method defined in an ancestor and
python_2_unicode_compatible decorator applied are flagged correctly as not
having explicitly defined __unicode__
"""
#  pylint: disable=missing-docstring

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class BaseModel(models.Model):
    def __str__(self):
        return 'Foo'


class SomeModel(BaseModel):  # [model-no-explicit-unicode]
    pass
