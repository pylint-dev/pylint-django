from itertools import chain

from astroid import (
    MANAGER, nodes, InferenceError, inference_tip,
    UseInferenceDefault
)
from astroid.nodes import ClassDef, Attribute

from pylint_django.utils import node_is_subclass


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


def _get_model_class_defs_from_module(module, model_name, module_name):
    class_defs = []
    for module_node in module.lookup(model_name)[1]:
        if (isinstance(module_node, nodes.ClassDef)
                and node_is_subclass(module_node, 'django.db.models.base.Model')):
            class_defs.append(module_node)
        elif isinstance(module_node, nodes.ImportFrom):
            imported_module = module_node.do_import_module()
            class_defs.extend(
                _get_model_class_defs_from_module(
                    imported_module, model_name, module_name
                )
            )
    return class_defs


def infer_key_classes(node, context=None):
    keyword_args = []
    if node.keywords:
        keyword_args = [kw.value for kw in node.keywords if kw.arg == 'to']
    all_args = chain(node.args, keyword_args)

    for arg in all_args:
        # typically the class of the foreign key will
        # be the first argument, so we'll go from left to right
        if isinstance(arg, (nodes.Name, nodes.Attribute)):
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
                # can be 'self' , 'Model' or 'app.Model'
                if arg.value == 'self':
                    module_name = ''
                    # for relations with `to` first parent be Keyword(arg='to')
                    # and we need to go deeper in parent tree to get model name
                    if isinstance(arg.parent, nodes.Keyword) and arg.parent.arg == 'to':
                        model_name = arg.parent.parent.parent.parent.name
                    else:
                        model_name = arg.parent.parent.parent.name
                else:
                    module_name, _, model_name = arg.value.rpartition('.')
            except AttributeError:
                break

            # when ForeignKey is specified only by class name we assume that
            # this class must be found in the current module
            if not module_name:
                current_module = node.frame()
                while not isinstance(current_module, nodes.Module):
                    current_module = current_module.parent.frame()

                module_name = current_module.name
            elif not module_name.endswith('models'):
                # otherwise Django allows specifying an app name first, e.g.
                # ForeignKey('auth.User') so we try to convert that to
                # 'auth.models', 'User' which works nicely with the `endswith()`
                # comparison below
                module_name += '.models'
                # ensure that module is loaded in astroid_cache, for cases when models is a package
                if module_name not in MANAGER.astroid_cache:
                    MANAGER.ast_from_module_name(module_name)

            # create list from dict_values, because it may be modified in a loop
            for module in list(MANAGER.astroid_cache.values()):
                # only load model classes from modules which match the module in
                # which *we think* they are defined. This will prevent infering
                # other models of the same name which are found elsewhere!
                if model_name in module.locals and module.name.endswith(module_name):
                    class_defs = _get_model_class_defs_from_module(
                        module, model_name, module_name
                    )

                    if class_defs:
                        return iter([class_defs[0].instantiate_class()])
    else:
        raise UseInferenceDefault
    return iter([key_cls.instantiate_class()])


def add_transform(manager):
    manager.register_transform(nodes.Call, inference_tip(infer_key_classes),
                               is_foreignkey_in_class)
