from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class Model(object):
    _meta = None
    objects = None

    id = None
    pk = None

    MultipleObjectsReturned = MultipleObjectsReturned

    save = lambda *a, **kw: None
    delete = lambda *a, **kw: None

# eliminate E1002 for Manager object
class Manager(object):
    get_queryset = lambda *a, **kw: None
    none = lambda *a, **kw: None
    all = lambda *a, **kw: None
    count = lambda *a, **kw: None
    dates = lambda *a, **kw: None
    distinct = lambda *a, **kw: None
    extra = lambda *a, **kw: None
    get = lambda *a, **kw: None
    get_or_create = lambda *a, **kw: None
    create = lambda *a, **kw: None
    bulk_create = lambda *a, **kw: None
    filter = lambda *a, **kw: None
    aggregate = lambda *a, **kw: None
    annotate = lambda *a, **kw: None
    complex_filter = lambda *a, **kw: None
    exclude = lambda *a, **kw: None
    in_bulk = lambda *a, **kw: None
    iterator = lambda *a, **kw: None
    latest = lambda *a, **kw: None
    order_by = lambda *a, **kw: None
    select_for_update = lambda *a, **kw: None
    select_related = lambda *a, **kw: None
    prefetch_related = lambda *a, **kw: None
    values = lambda *a, **kw: None
    values_list = lambda *a, **kw: None
    update = lambda *a, **kw: None
    reverse = lambda *a, **kw: None
    defer = lambda *a, **kw: None
    only = lambda *a, **kw: None
    using = lambda *a, **kw: None
    exists = lambda *a, **kw: None
