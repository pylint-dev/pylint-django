class Model(object):
    _meta = None
    objects = None

    id = None
    pk = None

    MultipleObjectsReturned = None
    DoesNotExist = None


# eliminate E1002 for Manager object
class Manager(object):
    pass
