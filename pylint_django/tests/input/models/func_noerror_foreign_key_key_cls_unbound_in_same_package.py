"""
Checks that Pylint does not crash with ForeignKey string reference pointing to model
in module of models package. See
https://github.com/PyCQA/pylint-django/issues/232

Note: the no-member disable is here b/c pylint-django doesn't know how to
load models.author.Author. When pylint-django tries to load models referenced
by a single string it assumes they are found in the same module it is inspecting.
Hence it can't find the Author class here so it tells us it doesn't have an
'id' attribute. Also see:
https://github.com/PyCQA/pylint-django/issues/232#issuecomment-495242695
"""
# pylint: disable=missing-docstring, no-member
from django.db import models


class FairyTail(models.Model):
    # fails with "UnboundLocalError: local variable 'key_cls' referenced before assignment"
    # when 'Author' model comes from same models package
    author = models.ForeignKey(to="Author", null=True, on_delete=models.CASCADE)

    def get_author_name(self):
        return self.author.id  # disable via no-member
