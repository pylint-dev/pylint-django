# pylint: disable=missing-docstring, line-too-long

import json

from django import http
from django.http import HttpResponse


def say_yes():
    return HttpResponse(json.dumps({"rc": 0, "response": "ok"}))  # [http-response-with-json-dumps]


def say_yes2():
    data = {"rc": 0, "response": "ok"}
    return http.HttpResponse(json.dumps(data))  # [http-response-with-json-dumps]


def say_no():
    return HttpResponse("no")


def redundant_content_type():
    data = {"rc": 0, "response": "ok"}
    return http.JsonResponse(data, content_type="application/json")  # [redundant-content-type-for-json-response]


def content_type_json():
    json_data = "this comes from somewhere"
    return HttpResponse(json_data, content_type="application/json")  # [http-response-with-content-type-json]
