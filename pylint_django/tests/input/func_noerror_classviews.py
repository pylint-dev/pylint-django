"""
Checks that Pylint does not complain about attributes and methods
when using Class-based Views
"""
#  pylint: disable=missing-docstring

from django.db import models
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic.edit import CreateView


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


class Book(models.Model):
    name = models.CharField(max_length=100)
    good = models.BooleanField(default=False)


class GetBook(DetailView):
    model = Book
    template_name = 'books/get.html'
    http_method_names = ['get']


class CreateBook(CreateView):
    model = Book
    template_name = 'books/new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New book'
        return context
