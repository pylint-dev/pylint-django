"""
Checks that Pylint does not complain about attributes and methods
when using Class-based Views
"""
#  pylint: disable=missing-docstring

from django.db import models
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import CreateView


class BoringView(TemplateView):
    # ensure that args, kwargs and request are not thrown up as errors
    def get_context_data(self, **kwargs):
        return {"request": self.request, "args": self.args, "kwargs": self.kwargs}


class JsonGetView(View):
    def get(self, request, *args, **kwargs):
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class JsonPostView(View):
    def post(self, request, *args, **kwargs):
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class JsonPutView(View):
    def put(self, request, *args, **kwargs):
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class JsonPatchView(View):
    def patch(self, request, *args, **kwargs):
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class JsonDeleteView(View):
    def delete(self, request, *args, **kwargs):
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class JsonHeadView(View):
    def head(self, request, *args, **kwargs):  # pylint: disable=method-hidden
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class JsonOptionsView(View):
    def options(self, request, *args, **kwargs):
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class JsonTraceView(View):
    def trace(self, request, *args, **kwargs):
        # do something with objects but don't use
        # self or request
        return JsonResponse({"rc": 0, "response": "ok"})


class Book(models.Model):
    name = models.CharField(max_length=100)
    good = models.BooleanField(default=False)


class GetBook(DetailView):
    model = Book
    template_name = "books/get.html"
    http_method_names = ["get"]


class CreateBook(CreateView):
    model = Book
    template_name = "books/new.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "New book"
        return context
