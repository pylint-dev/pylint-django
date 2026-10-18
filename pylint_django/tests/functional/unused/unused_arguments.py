"""
Checks that Pylint still complains about unused-arguments for other
arguments if a function/method contains an argument named `request`.
"""
# pylint: disable=missing-docstring

from django.http import JsonResponse
from django.views import View

# Pylint generates the warning `redefined-outer-name` if an argument name shadows
# a variable name from an outer scope. But if that argument name is ignored this
# warning will not be generated.
# Therefore define request here to cover this behaviour in this test case.

request = None  # pylint: disable=invalid-name


def user_detail(request, user_id):  # [unused-argument]
    # nothing is done with user_id
    return JsonResponse({"username": "steve"})


class UserView(View):
    def get(self, request, user_id):  # [unused-argument]
        # nothing is done with user_id
        return JsonResponse({"username": "steve"})


# The following views are already covered in other test cases.
# They are included here for completeness sake.


def welcome_view(request):
    # just don't use `request' b/c we could have Django views
    # which never use it!
    return JsonResponse({"message": "welcome"})


class CBV(View):
    def get(self, request):
        return JsonResponse({"message": "hello world"})
