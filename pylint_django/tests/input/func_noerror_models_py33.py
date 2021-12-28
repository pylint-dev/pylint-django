"""
Checks that Pylint does not complain about a fairly standard
Django Model
"""
#  pylint: disable=missing-docstring
from django.db import models


class SomeModel(models.Model):
    class Meta:
        pass

    some_field = models.CharField(max_length=20)

    other_fields = models.ManyToManyField("AnotherModel")

    def stuff(self):
        try:
            print(self._meta)
            print(self.other_fields.all()[0])
        except self.DoesNotExist:
            print("does not exist")
        except self.MultipleObjectsReturned:
            print("lala")

        print(self.get_some_field_display())


class SubclassModel(SomeModel):
    class Meta:
        pass
