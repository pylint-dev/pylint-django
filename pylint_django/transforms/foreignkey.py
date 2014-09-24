from astroid import nodes, InferenceError, Getattr


def swap_key_classes(node):
    if not isinstance(node.parent, nodes.Class):
        return

    # is this of the form  field = models.ForeignKey
    if not isinstance(node.value, nodes.CallFunc):
        return

    if isinstance(node.value.func, nodes.Getattr):
        attr = node.value.func.attrname
    elif isinstance(node.value.func, nodes.Name):
        attr = node.value.func.name
    else:
        return

    if attr not in ('OneToOneField', 'ForeignKey'):
        return

    for arg in node.value.args:
        # typically the class of the foreign key will
        # be the first argument, so we'll go from left to right
        if isinstance(arg, nodes.Name):
            try:
                key_cls = None
                for inferred in arg.infer():
                    key_cls = inferred
                    break
            except InferenceError:
                continue
            else:
                if key_cls is not None:
                    break
    else:
        return

    node.value = key_cls.instanciate_class()
    return node


def add_transform(manager):
    manager.register_transform(nodes.Assign, swap_key_classes)
