"""
Checks that Pylint doesn't raise an error when a 'ForeignKey' appears in a
non-django class

The real case is described as follow:
The project use tastypie and django.
tastypie has a `ForeignKey` field which has the same name
as django's `ForeignKey`.
The issue is the lint trys resolving the `ForeignKey` for the
tastypie `ForeignKey` which cause import error.
"""
from tastypie import fields
from tastypie.fields import ForeignKey

# pylint: disable=missing-docstring
from tastypie.resources import ModelResource


class MyTestResource(ModelResource):  # pylint: disable=too-few-public-methods
    field1 = ForeignKey("myapp.api.resource", "xxx")
    field2 = fields.ForeignKey("myapp.api.resource", "xxx")
