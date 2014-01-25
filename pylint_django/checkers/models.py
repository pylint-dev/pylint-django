import sys
from astroid.nodes import Assign, Function, AssName
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import check_messages
from pylint.checkers import BaseChecker
from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.utils import node_is_subclass


MESSAGES = {
    'E%d01' % BASE_ID: ("__unicode__ on a model must be callable (%s)",
                        'model-unicode-not-callable',
                        "Django models require a callable __unicode__ method"),
    'W%d01' % BASE_ID: ("No __unicode__ method on model (%s)",
                        'model-missing-unicode',
                        "Django models should implement a __unicode__ method for string representation"),
    'W%d02' % BASE_ID: ("Found __unicode__ method on model (%s). Python3 uses __str__.",
                        'model-has-unicode',
                        "Django models should not implement a __unicode__ method for string representation whan using Python3")
}


class ModelChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'django-model-checker'
    msgs = MESSAGES

    @check_messages('model-missing-unicode')
    def visit_class(self, node):
        if not node_is_subclass(node, 'django.db.models.base.Model'):
            # we only care about models
            return

        for child in node.get_children():
            if isinstance(child, Assign):
                grandchildren = list(child.get_children())
  
                if not isinstance(grandchildren[0], AssName):
                    continue

                name = grandchildren[0].name
                if name != '__unicode__':
                    continue

                assigned = grandchildren[1].infered()[0]
                if assigned.callable():
                    return

                self.add_message('E%s01' % BASE_ID, args=node.name, node=node)
                return

            if isinstance(child, Function) and child.name == '__unicode__':
                if sys.version_info.major >= 3:
                    self.add_message('W%s02' % BASE_ID, args=node.name, node=node)
                return

        # if we get here, then we have no __unicode__ method
        if sys.version_info.major >= 3:
            return

        self.add_message('W%s01' % BASE_ID, args=node.name, node=node)
