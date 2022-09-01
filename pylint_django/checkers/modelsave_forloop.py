from astroid.nodes import Call
from pylint import checkers, interfaces
from pylint.checkers import utils

from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.utils import node_is_subclass
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
        """
        for subnode in node.get_children():
            if not node_is_subclass(subnode, "django.db.models.base.Model",
                                    ".Model"):
                # We care about models only
                return
            for child in subnode.get_children():
                if isinstance(child, Call):
                    if child.func.as_string() == "create":
                        self.add_message(f"R{BASE_ID}01", node=child)
                    if child.func.as_string() == "save":
                        self.add_message(f"R{BASE_ID}02", node=child)
