"""
Checks that Pylint does not complain about django Forms
"""
#  pylint: disable=C0111,W5101,R0903

from django import forms


class TestForm(forms.Form):
    class Meta:
        pass

    some_field = forms.CharField()

    def clean(self):
        print self.cleaned_data
        print self.fields
        print self.error_class


class TestModelForm(forms.ModelForm):
    class Meta:
        pass
