# pylint: disable=model-no-explicit-str,model-no-explicit-str,missing-docstring,wrong-import-position
from django.db import models


class Author(models.Model):
    class Meta:
        app_label = 'test_app'
