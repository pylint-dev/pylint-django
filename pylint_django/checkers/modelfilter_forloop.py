from astroid.nodes import Attribute, Call, Expr
from pylint import checkers, interfaces
from pylint.checkers import utils

from pylint_django.__pkginfo__ import BASE_ID


class ModelFilterForLoopChecker(checkers.BaseChecker):
    """
    Checks for usage of "Model.manager.filter() inside of for loops
    """

    __implements__ = interfaces.IAstroidChecker

    name = "model-filter-forloop-checker"

    msgs = {
        f"R{BASE_ID}06": (
            "Consider using '__in' queries",
            "consider-using-in-queries",
            "Using 'Model.manager.filter()' or 'Model.manager.get() inside a "
            "for loop may negatively impact performance. Consider using a "
            "single query with as '__in' filter instead, outside of the loop.",
        ),
    }

    @utils.check_messages("consider-using-in-queries")
    def visit_for(self, node):
        """
        Checks for a Queryset.filter() inside of a for loop

        May create false positives
        """
        for subnode in node.body:
            for child in subnode.get_children():
                if isinstance(child, Expr):
                    for subchild in child.get_children():
                        if isinstance(subchild, Call):
                            self._check_forloop_filter(subchild)
                if isinstance(child, Call):
                    self._check_forloop_filter(child)

    def _check_forloop_filter(self, node):
        if isinstance(node.func, Attribute):
            # Ensure it's an attribute, to avoid clashing with the
            # filter() python builtin, may still clash with the dict .get()
            if node.func.attrname in ("filter", "get"):
                self.add_message(f"R{BASE_ID}06", node=node)
