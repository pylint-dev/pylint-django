"""
Checks that Pylint does not complain about django lazy proxy
when using ugettext_lazy
"""
from django.utils.translation import ugettext_lazy

ugettext_lazy('{something}').format(something='lala')
