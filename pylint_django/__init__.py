
from __future__ import absolute_import
import warnings

try:
    import django
except ImportError:
    from pylint_django import common as plugin
else:

    version = django.get_version()
    key = '_'.join(version.split('.')[:2])
    module_name = 'django_%s' % key

    try:
        this_module = __import__('pylint_django.%s' % module_name)
        plugin = getattr(this_module, module_name)
    except ImportError:
        warnings.warn("Django version %s is not directly supported, using defaults instead" % version)
        from pylint_django import common as plugin

register = plugin.register
