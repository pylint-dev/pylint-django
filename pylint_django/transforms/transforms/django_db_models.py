from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class Model(object):
    _meta = None
    objects = None

    id = None
    pk = None

    MultipleObjectsReturned = MultipleObjectsReturned
    DoesNotExist = ObjectDoesNotExist


# eliminate E1002 for Manager object
class Manager(object):
    pass
