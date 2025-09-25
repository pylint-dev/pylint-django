from astroid.nodes import Attribute, Call, Expr
from pylint import checkers
from pylint.checkers import utils

from pylint_django.__pkginfo__ import BASE_ID

# from pylint_django.augmentations import is_manager_attribute


class ModelSaveForLoopChecker(checkers.BaseChecker):
    """
    Checks for usage of Model.manager.create() or Model.save() inside of for
    loops
    """

    name = "model-save-forloop-checker"

    msgs = {
        f"R{BASE_ID}04": (
            "Consider using 'Model.bulk_create()'",
            "consider-using-bulk-create",
            "Using 'Model.manager.create()' inside a for loop may negatively "
            "impact performance. Consider using 'Model.manager.bulk_create()' "
            "instead.",
        ),
        f"R{BASE_ID}05": (
            "Consider using 'Model.bulk_*()",
            "consider-using-bulk-create-save",
            "Using 'Model.save()' inside a for loop may negatively impact "
            "performance. Consider using 'Model.manager.bulk_update()' or "
            "'Model.manager.bulk_create()' instead.",
        ),
    }

    @utils.only_required_for_messages("consider-using-bulk-create")
    @utils.only_required_for_messages("consider-using-bulk-create-save")
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
        if isinstance(node.func, Attribute):
            # Ensure node.func is an attribute to avoid crashes
            if node.func.attrname == "create":
                self.add_message(f"R{BASE_ID}04", node=node)
            if node.func.attrname == "save":
                self.add_message(f"R{BASE_ID}05", node=node)
