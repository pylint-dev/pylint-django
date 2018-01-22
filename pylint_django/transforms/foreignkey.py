from astroid import MANAGER, nodes, InferenceError, inference_tip, UseInferenceDefault
from pylint_django.utils import node_is_subclass
from pylint_django.compat import ClassDef, instantiate_class, Attribute


def is_foreignkey_in_class(node):
    # is this of the form  field = models.ForeignKey
    if not isinstance(node.parent, nodes.Assign):
        return False
    if not isinstance(node.parent.parent, ClassDef):
        return False

    if isinstance(node.func, Attribute):
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
        elif isinstance(arg, nodes.Const):
            try:
                model_name = arg.value.split('.')[-1]  # can be 'Model' or 'app.Model'
            except AttributeError:
                break

            for module in MANAGER.astroid_cache.values():
                if model_name in module.locals:
                    class_defs = [
                        module_node for module_node in module.lookup(model_name)[1]
                        if isinstance(module_node, nodes.ClassDef)
                        and node_is_subclass(module_node, 'django.db.models.base.Model')
                    ]
                    if class_defs:
                        return iter([instantiate_class(class_defs[0])()])
    else:
        raise UseInferenceDefault
    return iter([instantiate_class(key_cls)()])


def add_transform(manager):
    manager.register_transform(nodes.CallFunc, inference_tip(infer_key_classes),
                               is_foreignkey_in_class)
