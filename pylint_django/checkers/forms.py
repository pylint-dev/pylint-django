"""Models."""
from astroid.nodes import Assign, ClassDef

from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import check_messages
from pylint.checkers import BaseChecker

from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.utils import node_is_subclass


def _get_child_meta(node):
    for child in node.get_children():
        if isinstance(child, ClassDef) and child.name == 'Meta':
            return child
    return None


class FormChecker(BaseChecker):
    """Django model checker."""
    __implements__ = IAstroidChecker

    name = 'django-form-checker'
    msgs = {
        'W%d04' % BASE_ID: ("Use explicit fields instead of exclude in ModelForm",
                            'modelform-uses-exclude',
                            "Prevents accidentally allowing users to set fields, "
                            "especially when adding new fields to a Model")
    }

    @check_messages('modelform-uses-exclude')
    def visit_classdef(self, node):
        """Class visitor."""
        if not node_is_subclass(node, 'django.forms.models.ModelForm', '.ModelForm'):
            # we only care about forms
            return

        meta = _get_child_meta(node)

        if not meta:
            return

        for child in meta.get_children():
            if not isinstance(child, Assign):
                continue

            if child.targets[0].name == 'exclude':
                self.add_message('W%s04' % BASE_ID, node=child)
                break
