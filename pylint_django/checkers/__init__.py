from pylint_django.checkers.models import ModelChecker


def register_checkers(linter):
    linter.register_checker(ModelChecker(linter))
