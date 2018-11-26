# pylint: disable=super-init-not-called
from django.db.models.fields import files as django_fields


class FileField(django_fields.FieldFile, django_fields.FileField):
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        django_fields.FileField.__init__(verbose_name, name, upload_to, storage, **kwargs)


class ImageField(django_fields.ImageFieldFile, django_fields.ImageField):
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        django_fields.ImageField.__init__(verbose_name, name, width_field, height_field, **kwargs)
