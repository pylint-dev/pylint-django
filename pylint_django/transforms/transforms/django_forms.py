from django.forms import BaseForm, BaseModelForm


class Form(BaseForm):
    cleaned_data = None
    fields = None
    instance = None
    data = None
    _errors = None
    base_fields = None


class ModelForm(BaseModelForm):
    save_m2m = lambda: None
    cleaned_data = None
    fields = None
    instance = None
    data = None
    _errors = None
    base_fields = None
