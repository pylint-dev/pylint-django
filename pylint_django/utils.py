from astroid.exceptions import InferenceError
from astroid.bases import YES, Instance
from astroid.nodes import Class


def node_is_subclass(cls, subclass_name):
    if not isinstance(cls, (Class, Instance)):
        return False

    if cls.bases == YES:
        # ???
        return False
    for base_cls in cls.bases:
        try:
            for inf in base_cls.infered():
                if inf.qname() == subclass_name:
                    return True
        except InferenceError:
            pass