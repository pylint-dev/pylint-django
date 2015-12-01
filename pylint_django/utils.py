"""Utils."""
from astroid.exceptions import InferenceError
from astroid.bases import Instance
from astroid.nodes import Class
import sys

try:
    from astroid.bases import YES as Uninferable
except ImportError:
    try:
        from astroid.util import YES as Uninferable
    except ImportError:
        from astroid.util import Uninferable


PY3 = sys.version_info >= (3, 0)


def node_is_subclass(cls, *subclass_names):
    """Checks if cls node has parent with subclass_name."""
    if not isinstance(cls, (Class, Instance)):
        return False

    if cls.bases == Uninferable:
        return False
    for base_cls in cls.bases:
        try:
            for inf in base_cls.infered():
                if inf.qname() in subclass_names:
                    return True
                if inf != cls and node_is_subclass(inf, *subclass_names):
                    # check up the hierarchy in case we are a subclass of
                    # a subclass of a subclass ...
                    return True
        except InferenceError:
            continue

    return False
