
try:
    from astroid.nodes import ClassDef, FunctionDef, ImportFrom, AssignName, Attribute
except ImportError:
    from astroid.nodes import Class as ClassDef, \
        Function as FunctionDef, \
        From as ImportFrom, \
        AssName as AssignName, \
        Getattr as Attribute

try:
    from astroid.bases import YES as Uninferable
except ImportError:
    try:
        from astroid.util import YES as Uninferable
    except ImportError:
        from astroid.util import Uninferable


try:
    django = __import__('django')
    django_version = django.VERSION
except ImportError:
    # if not available, will be handled by the django_installed checker
    django_version = (1, 5)


def inferred(node):
    if hasattr(node, 'inferred'):
        return node.inferred
    else:
        return node.infered


def instantiate_class(node):
    if hasattr(node, 'instantiate_class'):
        return node.instantiate_class
    else:
        return node.instanciate_class
