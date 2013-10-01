"""
Checks that Pylint does not complain about attributes and methods
when creating a typical urls.py
"""
#  pylint: disable=C0111,R0903,W0232
__revision__ = ''

from django.views.generic import TemplateView


class BoringView(TemplateView):
    pass


from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^something', BoringView.as_view(), name='something'),
)
