"""
Checks that Pylint does not complain about django Forms
"""
#  pylint: disable=missing-docstring,wrong-import-position

from django import forms


class TestForm(forms.Form):
    class Meta:
        pass

    some_field = forms.CharField()

    def clean(self):
        print(self.cleaned_data)
        print(self.fields)
        print(self.error_class)


class TestModelForm(forms.ModelForm):
    class Meta:
        pass


class TestFormSubclass(forms.Form):
    class Meta:
        pass


class TestModelFormSubclass(forms.ModelForm):
    class Meta:
        pass
