"""
Checks that Pylint does not complain about attributes and methods
when creating a typical urls.py
"""
#  pylint: disable=C0111
#  pylint: disable=C0103
#    ^ eventually we should be able to override or update the
#      CONST_NAME_RGX value

from django.views.generic import TemplateView
from django.conf.urls import patterns, url


class BoringView(TemplateView):
    pass


urlpatterns = patterns('',
    url(r'^something', BoringView.as_view(), name='something'),
)
