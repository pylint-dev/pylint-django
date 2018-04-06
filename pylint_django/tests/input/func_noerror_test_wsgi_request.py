"""
Checks that Pylint does not complain about a standard test. See:
https://github.com/PyCQA/pylint-django/issues/78
"""

from django.test import TestCase
from django.db import models


class SomeModel(models.Model):
    """Just a model."""
    pass


class SomeTestCase(TestCase):
    """A test cast."""
    def test_thing(self):
        """Test a thing."""
        expected_object = SomeModel()
        response = self.client.get('/get/some/thing/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], expected_object)
