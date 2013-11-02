
class View(object):
    request = None
    args = None
    kwargs = None

    # as_view is marked as class-only
    def as_view(*args, **kwargs):
        pass
