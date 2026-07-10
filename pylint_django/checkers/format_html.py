# Licensed under the GPL 2.0: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint-django/blob/master/LICENSE
"""
Discourage building the format string of `format_html()` / `format_html_join()` and the
argument of `mark_safe()` by interpolation or concatenation.

Django's `format_html(format_string, *args, **kwargs)` HTML-escapes every argument before it is
substituted into the format string. When the format string is instead built with an f-string,
`str.format()`, `%`-formatting or `+` concatenation, the interpolated values are spliced in
without escaping, which reintroduces the XSS hole `format_html()` exists to close. The same is
true of `mark_safe()`, which performs no escaping at all.

Django deprecated calling `format_html()` without arguments for exactly this reason; see
https://code.djangoproject.com/ticket/34609 and the `format_html()` reference docs at
https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.format_html
"""

from __future__ import annotations

from astroid.nodes import Attribute, BinOp, Call, Const, FormattedValue, JoinedStr
from pylint import checkers
from pylint.checkers.utils import only_required_for_messages

from pylint_django.__pkginfo__ import BASE_ID


def _is_interpolated_string(node):
    """Return True when `node` is a string built by interpolation/concatenation.

    A plain string literal (or an f-string without any interpolation) is safe and returns False.
    """
    # f-string -- only flag when it actually interpolates a value.
    if isinstance(node, JoinedStr):
        return any(isinstance(value, FormattedValue) for value in node.values)

    if isinstance(node, BinOp):
        # "...%s..." % value
        if node.op == "%":
            return True
        # "..." + value + "..."
        if node.op == "+":
            operands = (node.left, node.right)
            has_const_str = any(isinstance(op, Const) and isinstance(op.value, str) for op in operands)
            has_dynamic = any(not isinstance(op, Const) for op in operands)
            return has_const_str and has_dynamic

    # "...{}...".format(value) or some_str.format(value)
    if isinstance(node, Call) and isinstance(node.func, Attribute) and node.func.attrname == "format":
        return True

    return False


class FormatHtmlChecker(checkers.BaseChecker):
    """
    Looks for interpolated strings passed to Django's HTML-escaping helpers, which silently
    bypasses their auto-escaping.
    """

    # configuration section name
    name = "format-html-checker"
    msgs = {
        f"W{BASE_ID}50": (
            "Pass interpolated values as arguments to format_html() instead of building the "
            "format string; arguments are automatically HTML-escaped",
            "format-html-interpolation",
            "Used when the format string of format_html()/format_html_join() is built with an "
            "f-string, str.format(), %-formatting or + concatenation, which bypasses escaping. "
            "See https://code.djangoproject.com/ticket/34609",
        ),
        f"W{BASE_ID}51": (
            "Avoid mark_safe() on a dynamically-built string; use format_html() with arguments "
            "so values are HTML-escaped",
            "mark-safe-interpolation",
            "Used when mark_safe() is called on a string built with an f-string, str.format(), "
            "%-formatting or + concatenation, which is not escaped at all. See "
            "https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.format_html",
        ),
    }

    @only_required_for_messages("format-html-interpolation", "mark-safe-interpolation")
    def visit_call(self, node):
        func = node.func.as_string()

        # Check the longer name first so format_html_join isn't swallowed by the format_html test.
        if func.endswith("format_html_join") and len(node.args) >= 2:
            candidate, message = node.args[1], "format-html-interpolation"
        elif func.endswith("format_html") and node.args:
            candidate, message = node.args[0], "format-html-interpolation"
        elif func.endswith("mark_safe") and node.args:
            candidate, message = node.args[0], "mark-safe-interpolation"
        else:
            return

        if _is_interpolated_string(candidate):
            self.add_message(message, node=node)
