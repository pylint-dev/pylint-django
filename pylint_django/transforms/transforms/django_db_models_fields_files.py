from django.db.models.fields import files as django_fields


class FileField(django_fields.FieldFile, django_fields.FileField):
    pass


class ImageField(django_fields.ImageFieldFile, django_fields.ImageField):
    pass
