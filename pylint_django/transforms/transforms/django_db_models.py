from django.core.exceptions import MultipleObjectsReturned \
    as MultipleObjectsReturnedException


def __noop(self, *args, **kwargs):
    """Just a dumb no-op function to make code a bit more DRY"""
    return None


class Model(object):
    _meta = None
    objects = None

    id = None
    pk = None

    MultipleObjectsReturned = MultipleObjectsReturnedException

    save = __noop
    delete = __noop


class Manager(object):
    """
    Eliminate E1002 for Manager object
    """
    get_queryset = __noop
    none = __noop
    all = __noop
    count = __noop
    dates = __noop
    distinct = __noop
    extra = __noop
    get = __noop
    get_or_create = __noop
    create = __noop
    bulk_create = __noop
    filter = __noop
    aggregate = __noop
    annotate = __noop
    complex_filter = __noop
    exclude = __noop
    in_bulk = __noop
    iterator = __noop
    latest = __noop
    order_by = __noop
    select_for_update = __noop
    select_related = __noop
    prefetch_related = __noop
    values = __noop
    values_list = __noop
    update = __noop
    reverse = __noop
    defer = __noop
    only = __noop
    using = __noop
    exists = __noop
