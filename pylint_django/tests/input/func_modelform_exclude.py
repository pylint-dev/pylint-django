"""
Checks that Pylint complains about ModelForm using exclude
"""
# pylint: disable=model-no-explicit-str,missing-docstring
from django import forms


class PersonForm(forms.ModelForm):
    class Meta:
        exclude = ('email',)  # [modelform-uses-exclude]
