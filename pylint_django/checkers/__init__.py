"""Checkers."""
from pylint_django.checkers.models import ModelChecker


def register_checkers(linter):
    """Register checkers."""
    linter.register_checker(ModelChecker(linter))
