"""
Test that django TextChoices does not raise a warning due to .label and .value methods
"""
#  pylint: disable=missing-docstring,too-few-public-methods

from django.db import models


class SomeTextChoices(models.TextChoices):
    CHOICE_A = ("choice_a", "Choice A")
    CHOICE_B = ("choice_b", "Choice B")
    CHOICE_C = ("choice_c", "Choice C")


class SomeClass():
    choice_values = [
        SomeTextChoices.CHOICE_A.value,
        SomeTextChoices.CHOICE_B.value,
    ]
    choice_labels = [
        SomeTextChoices.CHOICE_B.label,
        SomeTextChoices.CHOICE_C.label,
    ]
