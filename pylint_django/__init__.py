"""pylint_django module."""
from __future__ import absolute_import

import sys
import warnings

from pylint_django import plugin

if sys.version_info < (3, ):
    warnings.warn("Version 0.8.0 is the last to support Python 2. "
                  "Please migrate to Python 3!", DeprecationWarning)

register = plugin.register
