from astroid.nodes import Attribute, Call
from pylint import checkers
from pylint.checkers import utils

from pylint_django.__pkginfo__ import BASE_ID

# from pylint_django.augmentations import is_manager_attribute


class QuerysetIteratorForLoopChecker(checkers.BaseChecker):
    """
    Checks for usage of "QuerySet.all()" in the head of a for loop,
    eventually suggesting the usage of ".iterator()"
    """

    name = "queryset-iterator-forloop-checker"

    msgs = {
        f"R{BASE_ID}07": (
            "Consider using 'Queryset.iterator()'",
            "consider-using-queryset-iterator",
            "Using 'QuerySet.all()' may load all results in memory "
            "if you need to iterate over the data only once and don't need "
            "caching, 'QuerySet.iterator()' may be a more performant option.",
        ),
    }

    @utils.only_required_for_messages("consider-using-queryset-iterator")
    def visit_for(self, node):
        """
        Checks for a QuerySet.all() inside of a for loop

        May create false positives
        """
        for subnode in node.get_children():
            if isinstance(subnode, Call):
                if isinstance(subnode.func, Attribute):
                    # Ensure it's an attribute, to avoid clashing with the
                    # all() python builtin
                    if subnode.func.attrname == "all":
                        self.add_message(f"R{BASE_ID}07", node=subnode)
