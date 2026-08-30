from astroid import MANAGER, scoped_nodes, nodes, inference_tip

from pylint_django import utils

class_names = set()

def is_tuple_in_text_choices(node):
    # file_name = node.root().file
    # if file_name not in file_names:
    #     file_names.update({file_name})
    #     import ipdb; ipdb.set_trace()
    # else:
    #     return False

    if not (isinstance(node.parent, nodes.Assign)
            or isinstance(node.parent, nodes.FunctionDef)) :
        return False
    if not isinstance(node.parent.parent, nodes.ClassDef):
        return False
    if "TextChoices" in [i.name for i in node.parent.parent.bases]:
        import ipdb; ipdb.set_trace()

    class_name = node.parent.parent.name
    if class_name not in class_names:
        class_names.update({class_name})
        # import ipdb; ipdb.set_trace()
    else:
        return False
    
    # if node.parent.parent.name == "SomeTextChoices":
    #     import ipdb; ipdb.set_trace()
    # else:
    #     return False

    # if node.parent.parent.parent.name in ["TextChoices", "SomeClass", "ChoicesMeta", "TextChoices"]:
    #     import ipdb; ipdb.set_trace()
    # else:
    #     return False

    # if node.root().file.endswith("enums.py"):
    #     import ipdb; ipdb.set_trace()
    # else:
    #     return False

    # try:
    #     if node.root().file.endswith("model_enum.py"):
    #         import ipdb; ipdb.set_trace()
    # except:
    #     import ipdb; ipdb.set_trace()
    # if (node.parent.parent.name != "LazyObject"
    #         and node.parent.parent.parent.name != "django.db.models.expressions"
    #         and node.parent.parent.parent.name != "django.db.models.fields"):
    #     import ipdb; ipdb.set_trace()

    if isinstance(node.func, nodes.Attribute):
        attr = node.func.attrname
    elif isinstance(node.func, nodes.Name):
        attr = node.func.name
    else:
        return False
    return True


def infer_key_classes(node, context=None):
    pass


def add_transforms(manager):
    manager.register_transform(nodes.Call, inference_tip(infer_key_classes),
                               is_tuple_in_text_choices)
