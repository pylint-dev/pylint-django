"""
Checks that Pylint does not complain about foreign key sets on models
"""
#  pylint: disable=missing-docstring

from django.db import models


class SomeModel(models.Model):
    name = models.CharField(max_length=20)

    def get_others(self):
        return self.othermodel_set.all()

    def get_first(self):
        return self.othermodel_set.first()


class OtherModel(models.Model):
    count = models.IntegerField()
    something = models.ForeignKey(SomeModel, on_delete=models.CASCADE)


class ThirdModel(models.Model):
    whatever = models.ForeignKey(SomeModel, related_name='whatevs',
                                 on_delete=models.CASCADE)


def count_whatevers():
    if SomeModel().whatevs.exists():
        return SomeModel().whatevs.count()
    return -1
