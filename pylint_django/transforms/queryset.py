from astroid import MANAGER, nodes, inference_tip
from astroid.nodes import Attribute

from pylint_django import utils


# function calls of a django.db.models.Manager that return a django.db.models.QuerySet
QUERYSET_FUNCS = (
    'get_queryset',
    'filter',
    'all',
)


def is_queryset_producing_call(node):

    if isinstance(node.func, Attribute):
        # TODO here, this currently identifies ANY attribute named 'filter'
        # not just the one on Managers/QuerySets
        if node.func.attrname in QUERYSET_FUNCS:
            return True

    return False


def infer_queryset(call_node, context=None):

    base_nodes = MANAGER.ast_from_module_name('django.db.models.query').lookup('QuerySet')

    if utils.PY3:
        base_nodes = [n for n in base_nodes[1] if not isinstance(n, nodes.ImportFrom)]
    else:
        base_nodes = list(base_nodes[1])

    return iter([node.instantiate_class() for node in base_nodes])


def add_transforms(manager):

    manager.register_transform(nodes.Call,
                               inference_tip(infer_queryset),
                               is_queryset_producing_call)
