# flake8: noqa
# pylint: skip-file
# no sane linter can figure out the hackiness in this compatability layer...

try:
    from astroid.nodes import ClassDef, FunctionDef, ImportFrom, AssignName, Attribute
except ImportError:
    from astroid.nodes import (
        Class as ClassDef,
        Function as FunctionDef,
        From as ImportFrom,
        AssName as AssignName,
        Getattr as Attribute,
    )

# pylint 2.04->2.2 : YES was renamed to Uninferable, then YES became deprecated, then was removed
try:
    from astroid.bases import YES as Uninferable
except ImportError:
    try:
        from astroid.util import YES as Uninferable
    except ImportError:
        from astroid.util import Uninferable

import pylint

# pylint before version 2.3 does not support load_configuration() hook.
LOAD_CONFIGURATION_SUPPORTED = False
try:
    LOAD_CONFIGURATION_SUPPORTED = tuple(pylint.__version__.split('.')) >= ('2', '3')
except AttributeError:
    LOAD_CONFIGURATION_SUPPORTED = pylint.__pkginfo__.numversion >= (2, 3)
