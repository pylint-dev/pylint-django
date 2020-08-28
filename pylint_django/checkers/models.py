"""Models."""
from astroid import Const
from astroid.nodes import Assign
from astroid.nodes import ClassDef, FunctionDef, AssignName

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages

from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.utils import node_is_subclass


MESSAGES = {
    "E%d01"
    % BASE_ID: (
        "__str__ on a model must be callable (%s)",
        "model-str-not-callable",
        "Django models require a callable __str__ method",
    ),
    "W%d01"
    % BASE_ID: (
        "No __str__ method on model (%s)",
        "model-missing-str",
        "Django models should implement a __str__ method for string representation "
        "(see https://docs.djangoproject.com/en/3.1/ref/models/instances/#django.db.models.Model.__str__)",
    ),
    "W%d02"
    % BASE_ID: (
        "Found __unicode__ method on model (%s). Python3 uses __str__.",
        "model-has-unicode",
        "Django models should not implement a __unicode__ "
        "method for string representation when using Python3",
    ),
    "W%d03"
    % BASE_ID: (
        "Model does not explicitly define __str__ (%s)",
        "model-no-explicit-str",
        "Django models should implement a __str__ method for string representation. "
        "A parent class of this model does, but ideally all models should be explicit.",
    ),
}


def _is_meta_with_abstract(node):
    if isinstance(node, ClassDef) and node.name == "Meta":
        for meta_child in node.get_children():
            if not isinstance(meta_child, Assign):
                continue
            if not meta_child.targets[0].name == "abstract":
                continue
            if not isinstance(meta_child.value, Const):
                continue
                # TODO: handle tuple assignment?
            # eg:
            #    abstract, something_else = True, 1
            if meta_child.value.value:
                # this class is abstract
                return True
    return False


class ModelChecker(BaseChecker):
    """Django model checker."""

    __implements__ = IAstroidChecker

    name = "django-model-checker"
    msgs = MESSAGES

    @check_messages("model-str-not-callable", "model-missing-str", "model-has-unicode", "model-no-explicit-str")
    def visit_classdef(self, node):
        """Class visitor."""
        if not node_is_subclass(node, "django.db.models.base.Model", ".Model"):
            # we only care about models
            return

        for child in node.get_children():
            if _is_meta_with_abstract(child):
                return

            if isinstance(child, Assign):
                grandchildren = list(child.get_children())

                if not isinstance(grandchildren[0], AssignName):
                    continue

                name = grandchildren[0].name
                if name != "__str__":
                    continue

                grandchild = grandchildren[1]
                assigned = grandchild.inferred()[0]

                if assigned.callable():
                    return

                self.add_message("E%s01" % BASE_ID, args=node.name, node=node)
                return

            if isinstance(child, FunctionDef) and child.name == "__unicode__":
                self.add_message("W%s02" % BASE_ID, args=node.name, node=node)
                return

        # a different warning is emitted if a parent declares __unicode__
        for method in node.methods():
            if method.name != '__str__':
                # only looking for __str__ methods
                continue

            if method.parent == node:
                # this model declares a __str__ method so we can stop checking
                return

            elif method.parent != node:
                # this happens if a parent declares the str method but
                # this node does not
                self.add_message("W%s03" % BASE_ID, args=node.name, node=node)
                return

        # if we get here, we have no __str__ method at all, although this is unlikely
        # since the Django BaseModel does, but still.
        self.add_message("W%s01" % BASE_ID, args=node.name, node=node)
