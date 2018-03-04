"""
Checks that Pylint does not complain about DRF serializers
"""
#  pylint: disable=C0111,W5101

from rest_framework import serializers

class TestSerializerSubclass(serializers.ModelSerializer):
    class Meta:
        pass
