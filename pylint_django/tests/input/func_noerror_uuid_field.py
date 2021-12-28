"""
Checks that Pylint does not complain about UUID fields.
"""
#  pylint: disable=missing-class-docstring,missing-function-docstring
from __future__ import print_function

from django.db import models


class LotsOfFieldsModel(models.Model):
    uuidfield = models.UUIDField()

    def uuidfield_tests(self):
        print(self.uuidfield.bytes)
        print(self.uuidfield.bytes_le)
        print(self.uuidfield.fields[2])
        print(self.uuidfield.hex)
        # print(self.uuidfield.int)  # Don't know how to properly check this one
        print(self.uuidfield.variant)
        print(self.uuidfield.version)
