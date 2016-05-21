class View(object):
    request = None
    args = ()
    kwargs = {}

    # as_view is marked as class-only
    def as_view(*args, **kwargs):
        pass
