from astroid.nodes import Call, Expr
from pylint import checkers, interfaces
from pylint.checkers import utils

from pylint_django.__pkginfo__ import BASE_ID
# from pylint_django.augmentations import is_manager_attribute


class ModelSaveForLoopChecker(checkers.BaseChecker):
    __implements__ = (interfaces.IAstroidChecker)

    name = "model-save-forloop-checker"

    msgs = {
        f"R{BASE_ID}04": (
            "'Model.create()' in for loop",
            "model-create-in-forloop",
            "Using 'Model.create()' inside a for loop may impact performance. "
            "Use 'Model.bulk_create()' instead."
        ),
        f"R{BASE_ID}05": (
            "'Model.save()' in for loop",
            "model-save-in-forloop",
            "Using 'Model.save()' inside a for loop may impact performance. "
            "Use 'Model.bulk_update()' or 'Model.bulk_create()' instead."
        ),
    }

    @utils.check_messages("model-save-in-forloop")
    @utils.check_messages("model-create-in-forloop")
    def visit_for(self, node):
        """
        Checks for a Model.create() inside of a for loop

        May create false positives
        """
        for subnode in node.body:
            for child in subnode.get_children():
                if isinstance(child, Expr):
                    for subchild in child.get_children():
                        if isinstance(subchild, Call):
                            self._check_forloop_create_save(subchild)
                if isinstance(child, Call):
                    self._check_forloop_create_save(child)

    def _check_forloop_create_save(self, node):
        if node.func.attrname == "create":
            self.add_message(f"R{BASE_ID}04", node=node)
        if node.func.attrname == "save":
            self.add_message(f"R{BASE_ID}05", node=node)
