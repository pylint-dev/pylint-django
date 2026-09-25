"""
Checks that Pylint does not emit no-member when a subclass of a shimmed
model field calls a `Field` method through `super()`.

The type shim in `pylint_django.transforms.fields` replaces a field's inferred
bases with the runtime type it behaves like (`str` for CharField, `uuid.UUID`
for UUIDField, and so on). `Field` itself has to stay in that list, or every
method defined on it -- `pre_save`, `get_prep_value`, `contribute_to_class`,
`get_default`, `clean` -- disappears from the MRO that `super()` resolves
against, and each call raises a false E1101.
"""
#  pylint: disable=missing-class-docstring,missing-function-docstring

from django.db import models


class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value:
            return value[: self.max_length]
        return value

    def clean(self, value, model_instance):
        cleaned = super().clean(value, model_instance)
        return cleaned.strip()


class OffsetIntegerField(models.IntegerField):
    def get_default(self):
        return super().get_default() or 0

    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only=private_only)
        setattr(cls, f"{name}_offset", 1)


class UuidField(models.UUIDField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value is None and add:
            return self.get_default()
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("default", None)
        return name, path, args, kwargs


class StampedDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        print(value)
        return value


class DefaultingJSONField(models.JSONField):
    def get_default(self):
        default = super().get_default()
        return default if default else {}
