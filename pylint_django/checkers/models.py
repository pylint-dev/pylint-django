"""Models."""
from astroid import Const
from astroid.nodes import Assign, AssignName, ClassDef, FunctionDef
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker

from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.utils import PY3, node_is_subclass

MESSAGES = {
    f"E{BASE_ID}01": (
        "__unicode__ on a model must be callable (%s)",
        "model-unicode-not-callable",
        "Django models require a callable __unicode__ method",
    ),
    f"W{BASE_ID}01": (
        "No __unicode__ method on model (%s)",
        "model-missing-unicode",
        "Django models should implement a __unicode__ method for string representation",
    ),
    f"W{BASE_ID}02": (
        "Found __unicode__ method on model (%s). Python3 uses __str__.",
        "model-has-unicode",
        "Django models should not implement a __unicode__ method for string representation when using Python3",
    ),
    f"W{BASE_ID}03": (
        "Model does not explicitly define __unicode__ (%s)",
        "model-no-explicit-unicode",
        "Django models should implement a __unicode__ method for string representation. "
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


def _has_python_2_unicode_compatible_decorator(node):
    if node.decorators is None:
        return False

    for decorator in node.decorators.nodes:
        if getattr(decorator, "name", None) == "python_2_unicode_compatible":
            return True

    return False


def _is_unicode_or_str_in_python_2_compatibility(method):
    if method.name == "__unicode__":
        return True

    if method.name == "__str__" and _has_python_2_unicode_compatible_decorator(method.parent):
        return True

    return False


class ModelChecker(BaseChecker):
    """Django model checker."""

    __implements__ = IAstroidChecker

    name = "django-model-checker"
    msgs = MESSAGES

    @check_messages("model-missing-unicode")
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
                if name != "__unicode__":
                    continue

                grandchild = grandchildren[1]
                assigned = grandchild.inferred()[0]

                if assigned.callable():
                    return

                self.add_message(f"E{BASE_ID}01", args=node.name, node=node)
                return

            if isinstance(child, FunctionDef) and child.name == "__unicode__":
                if PY3:
                    self.add_message(f"W{BASE_ID}02", args=node.name, node=node)
                return

        # if we get here, then we have no __unicode__ method directly on the class itself

        # a different warning is emitted if a parent declares __unicode__
        for method in node.methods():
            if method.parent != node and _is_unicode_or_str_in_python_2_compatibility(method):
                # this happens if a parent declares the unicode method but
                # this node does not
                self.add_message(f"W{BASE_ID}03", args=node.name, node=node)
                return

        # if the Django compatibility decorator is used then we don't emit a warning
        # see https://github.com/PyCQA/pylint-django/issues/10
        if _has_python_2_unicode_compatible_decorator(node):
            return

        if PY3:
            return

        self.add_message(f"W{BASE_ID}01", args=node.name, node=node)
