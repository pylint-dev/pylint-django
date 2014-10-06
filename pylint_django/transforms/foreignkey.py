from astroid import nodes, InferenceError, inference_tip, UseInferenceDefault


def is_foreignkey_in_class(node):
    # is this of the form  field = models.ForeignKey
    if not isinstance(node.parent, nodes.Assign):
        return False
    if not isinstance(node.parent.parent, nodes.Class):
        return False

    if isinstance(node.func, nodes.Getattr):
        attr = node.func.attrname
    elif isinstance(node.func, nodes.Name):
        attr = node.func.name
    else:
        return False
    return attr in ('OneToOneField', 'ForeignKey')


def infer_key_classes(node, context=None):
    for arg in node.args:
        # typically the class of the foreign key will
        # be the first argument, so we'll go from left to right
        if isinstance(arg, (nodes.Name, nodes.Getattr)):
            try:
                key_cls = None
                for inferred in arg.infer(context=context):
                    key_cls = inferred
                    break
            except InferenceError:
                continue
            else:
                if key_cls is not None:
                    break
    else:
        raise UseInferenceDefault
    return iter([key_cls.instanciate_class()])


def add_transform(manager):
    manager.register_transform(nodes.CallFunc, inference_tip(infer_key_classes),
                               is_foreignkey_in_class)
