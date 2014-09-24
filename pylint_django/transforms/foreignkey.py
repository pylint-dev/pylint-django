from astroid import nodes


def do_stuff(*args, **kwargs):
    import pdb; pdb.set_trace()


def add_transform(manager):
    manager.register_transform(nodes.Class, do_stuff)