"""
Checks that Pylint does not complain about DRF viewsets
"""
#  pylint: disable=C0111,W5101,use-symbolic-message-instead,import-error,too-few-public-methods

from rest_framework import viewsets


class TestModelViewsetSubclass(viewsets.ModelViewset):
    pass
