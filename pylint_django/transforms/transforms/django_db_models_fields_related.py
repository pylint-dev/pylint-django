from django.db.models.query import QuerySet
from django.db.models.fields.related import ManyToManyField as ManyToManyFieldOriginal


class ManyToManyField(ManyToManyFieldOriginal, QuerySet):
    def __init__(self, to, **kwargs):
        ManyToManyFieldOriginal.__init__(to, **kwargs)
        self.model = None
        self.query_field_name = ''
        self.core_filters = {}
        self.instance = None
        self.symmetrical = None
        self.source_field = None
        self.source_field_name = ''
        self.target_field_name = ''
        self.reverse = None
        self.through = None
        self.prefetch_cache_name = None
        self.related_val = None

    def get_queryset(self):
        pass

    def get_prefetch_queryset(self, instances):
        pass

    def add(self, *objs):
        pass

    def create(self, **kwargs):
        pass

    def get_or_create(self, **kwargs):
        pass

    def remove(self, *objs):
        pass

    def clear(self):
        pass
