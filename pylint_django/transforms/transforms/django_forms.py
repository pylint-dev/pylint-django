from django.forms import BaseForm, BaseModelForm


class Form(BaseForm):
    cleaned_data = None
    fields = None
    instance = None
    data = None
    _errors = None
    base_fields = None


class ModelForm(BaseModelForm):
    def save_m2m(self):
        return None
    cleaned_data = None
    fields = None
    instance = None
    data = None
    _errors = None
    base_fields = None
