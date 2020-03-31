"""
Checks that Pylint does not complain about django lazy proxy
when using gettext_lazy
"""
from django.utils.translation import gettext_lazy

gettext_lazy('{something}').format(something='lala')
