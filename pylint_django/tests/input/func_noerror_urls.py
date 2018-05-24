"""
Checks that Pylint does not complain about attributes and methods
when creating a typical urls.py
"""
#  pylint: disable=missing-docstring

from django.views.generic import TemplateView
from django.conf.urls import url


class BoringView(TemplateView):
    pass


urlpatterns = [
    url(r'^something',
        BoringView.as_view(),
        name='something'),
]
