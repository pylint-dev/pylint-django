from django.db.models.query import QuerySet
from django.db.models.fields.related import ManyToManyField as ManyToManyFieldOriginal


class ManyToManyField(ManyToManyFieldOriginal, QuerySet):
    def __init__(self, to, **kwargs):
        ManyToManyFieldOriginal.__init__(to, **kwargs)
