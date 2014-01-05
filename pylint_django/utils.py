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
                if node_is_subclass(inf, subclass_name):
                    # check up the hierachy in case we are a subclass of
                    # a subclass of a subclass ...
                    return True
        except InferenceError:
            pass

    return False