from pylint import checkers

from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.compat import check_messages


class AuthUserChecker(checkers.BaseChecker):
    name = "auth-user-checker"

    msgs = {
        f"E{BASE_ID}41": (
            "Hard-coded 'auth.User'",
            "hard-coded-auth-user",
            "Don't hard-code the auth.User model. Use settings.AUTH_USER_MODEL instead!",
        ),
        f"E{BASE_ID}42": (
            "User model imported from django.contrib.auth.models",
            "imported-auth-user",
            "Don't import django.contrib.auth.models.User model. Use django.contrib.auth.get_user_model() instead!",
        ),
    }

    @check_messages("hard-coded-auth-user")
    def visit_const(self, node):
        # for now we don't check if the parent is a ForeignKey field
        # because the user model should not be hard-coded anywhere
        if node.value == "auth.User":
            self.add_message("hard-coded-auth-user", node=node)

    @check_messages("imported-auth-user")
    def visit_importfrom(self, node):
        if node.modname == "django.contrib.auth.models":
            for imported_names in node.names:
                if imported_names[0] in ["*", "User"]:
                    self.add_message("imported-auth-user", node=node)
                    break
