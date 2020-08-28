"""
Checks that Pylint does not complain about DRF serializers
"""
# pylint: disable=model-no-explicit-str,C0111,W5101

from rest_framework import serializers


class TestSerializerSubclass(serializers.ModelSerializer):
    class Meta:
        pass
