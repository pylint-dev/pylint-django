"""Utils."""
import sys

import astroid
from astroid.bases import Instance
from astroid.exceptions import InferenceError
from astroid.nodes import ClassDef

from pylint_django.compat import Uninferable

PY3 = sys.version_info >= (3, 0)  # TODO: pylint_django doesn't support Py2 any more


def node_is_subclass(cls, *subclass_names):
    """Checks if cls node has parent with subclass_name."""
    if not isinstance(cls, (ClassDef, Instance)):
        return False

    if cls.bases == Uninferable:
        return False
    for base_cls in cls.bases:
        try:
            for inf in base_cls.inferred():
                if inf.qname() in subclass_names:
                    return True
                if inf != cls and node_is_subclass(inf, *subclass_names):
                    # check up the hierarchy in case we are a subclass of
                    # a subclass of a subclass ...
                    return True
        except InferenceError:
            continue

    return False


def is_migrations_module(node):
    if not isinstance(node, astroid.Module):
        return False

    return "migrations" in node.path[0] and not node.path[0].endswith("__init__.py")
