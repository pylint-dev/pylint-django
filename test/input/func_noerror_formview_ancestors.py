"""
Checks that Pylint does not complain about django FormViews
having too many ancestors
"""
#  pylint: disable=missing-docstring
from django.views.generic import FormView


class SomeView(FormView):
    pass
