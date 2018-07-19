"""
Checks that Pylint does not complain about Manager methods returning lists
when they in fact return QuerySets
"""

from django.db import models


class SomeModelQuerySet(models.QuerySet):
    """ A missing docstring """
    @staticmethod
    def public_method():
        """ A missing docstring """
        return 1


class SomeModelManager(models.Manager):
    """A missing docstring"""

    @staticmethod
    def public_method():
        """ A missing docstring """
        return 1

    @staticmethod
    def another_public_method():
        """ A missing docstring """
        return 1


class SomeModel(models.Model):
    """ A missing docstring """

    name = models.CharField(max_length=20)
    datetimestamp = models.DateTimeField()

    objects = SomeModelManager()


class OtherModel(models.Model):
    """ A missing docstring """

    name = models.CharField(max_length=20)
    somemodel = models.ForeignKey(SomeModel, on_delete=models.CASCADE, null=False)


def call_some_querysets():
    """ A missing docstring """

    not_a_list = SomeModel.objects.filter()
    not_a_list.values_list('id', flat=True)
