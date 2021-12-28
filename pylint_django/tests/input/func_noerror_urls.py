"""
Checks that Pylint does not complain about attributes and methods
when creating a typical urls.py
"""
#  pylint: disable=missing-docstring

try:
    # to be able to test django versions from 1.11 - 3.2
    from django.urls import path
except ImportError:
    from django.conf.urls import url as path
from django.views.generic import TemplateView


class BoringView(TemplateView):
    pass


urlpatterns = [
    path(r"^something", BoringView.as_view(), name="something"),
]
