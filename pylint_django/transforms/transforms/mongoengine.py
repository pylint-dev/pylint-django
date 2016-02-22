from mongoengine.errors import DoesNotExist, MultipleObjectsReturned

class Document(object):
    _meta = None
    objects = None

    id = None
    pk = None

    MultipleObjectsReturned = MultipleObjectsReturned
    DoesNotExist = DoesNotExist

    save = lambda: None
