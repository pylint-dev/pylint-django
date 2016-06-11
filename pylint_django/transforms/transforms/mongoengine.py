from mongoengine.errors import DoesNotExist, MultipleObjectsReturned
from mongoengine.queryset.manager import QuerySetManager

class Document(object):
    _meta = None
    objects = QuerySetManager()

    id = None
    pk = None

    MultipleObjectsReturned = MultipleObjectsReturned
    DoesNotExist = DoesNotExist

    save = lambda: None
