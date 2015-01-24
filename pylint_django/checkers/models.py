"""Models."""
from astroid import Const
from astroid.nodes import Assign, Function, AssName, Class
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import check_messages
from pylint.checkers import BaseChecker
from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.utils import node_is_subclass, PY3


MESSAGES = {
    'E%d01' % BASE_ID: ("__unicode__ on a model must be callable (%s)",
                        'model-unicode-not-callable',
                        "Django models require a callable __unicode__ method"),
    'W%d01' % BASE_ID: ("No __unicode__ method on model (%s)",
                        'model-missing-unicode',
                        "Django models should implement a __unicode__ method for string representation"),
    'W%d02' % BASE_ID: ("Found __unicode__ method on model (%s). Python3 uses __str__.",
                        'model-has-unicode',
                        "Django models should not implement a __unicode__ "
                        "method for string representation when using Python3"),
    'W%d03' % BASE_ID: ("Model does not explicitly define __unicode__ (%s)",
                        'model-no-explicit-unicode',
                        "Django models should implement a __unicode__ method for string representation. "
                        "A parent class of this model does, but ideally all models should be explicit.")
}


def _is_meta_with_abstract(node):
    if isinstance(node, Class) and node.name == 'Meta':
        for meta_child in node.get_children():
            if not isinstance(meta_child, Assign):
                continue
            if not meta_child.targets[0].name == 'abstract':
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

    name = 'django-model-checker'
    msgs = MESSAGES

    @check_messages('model-missing-unicode')
    def visit_class(self, node):
        """Class visitor."""
        if not node_is_subclass(node, 'django.db.models.base.Model'):
            # we only care about models
            return

        for child in node.get_children():
            if _is_meta_with_abstract(child):
                return

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
                if PY3:
                    self.add_message('W%s02' % BASE_ID, args=node.name, node=node)
                return

        # if we get here, then we have no __unicode__ method directly on the class itself
        if PY3:
            return

        # a different warning is emitted if a parent declares __unicode__
        for method in node.methods():
            if method.name == '__unicode__':
                # this happens if a parent declares the unicode method but
                # this node does not
                self.add_message('W%s03' % BASE_ID, args=node.name, node=node)
                return

        # if the Django compatibility decorator is used then we don't emit a warning
        # see https://github.com/landscapeio/pylint-django/issues/10
        if node.decorators is not None:
            for decorator in node.decorators.nodes:
                if getattr(decorator, 'name', None) == 'python_2_unicode_compatible':
                    return

        self.add_message('W%s01' % BASE_ID, args=node.name, node=node)
