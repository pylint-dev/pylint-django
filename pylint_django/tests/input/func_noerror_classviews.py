"""
Checks that Pylint does not complain about attributes and methods
when using Class-based Views
"""
#  pylint: disable=missing-docstring

from django.http import JsonResponse
from django.views.generic import TemplateView, View


class BoringView(TemplateView):
    # ensure that args, kwargs and request are not thrown up as errors
    def get_context_data(self, **kwargs):
        return {
            'request': self.request,
            'args': self.args,
            'kwargs': self.kwargs
        }


class JsonView(View):
    def post(self, request):
        # do something with objects but don't use
        # self or request
        return JsonResponse({'rc': 0, 'response': 'ok'})
