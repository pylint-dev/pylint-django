# flake8: noqa
# pylint: skip-file
# no sane linter can figure out the hackiness in this compatibility layer...

try:
    from astroid.nodes import AssignName, Attribute, ClassDef, FunctionDef, ImportFrom
except ImportError:
    from astroid.nodes import AssName as AssignName
    from astroid.nodes import Class as ClassDef
    from astroid.nodes import From as ImportFrom
    from astroid.nodes import Function as FunctionDef
    from astroid.nodes import Getattr as Attribute

# pylint 2.04->2.2 : YES was renamed to Uninferable, then YES became deprecated, then was removed
try:
    from astroid.bases import YES as Uninferable
except ImportError:
    try:
        from astroid.util import YES as Uninferable
    except ImportError:
        from astroid.util import Uninferable

try:
    from pylint.checkers.utils import check_messages
except (ImportError, ModuleNotFoundError):
    from pylint.checkers.utils import only_required_for_messages as check_messages

import pylint

# pylint before version 2.3 does not support load_configuration() hook.
LOAD_CONFIGURATION_SUPPORTED = False
try:
    LOAD_CONFIGURATION_SUPPORTED = tuple(pylint.__version__.split(".")) >= ("2", "3")
except AttributeError:
    LOAD_CONFIGURATION_SUPPORTED = pylint.__pkginfo__.numversion >= (2, 3)
