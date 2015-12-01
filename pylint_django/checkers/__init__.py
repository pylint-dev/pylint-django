"""Checkers."""
from pylint_django.checkers.django_installed import DjangoInstalledChecker
from pylint_django.checkers.models import ModelChecker


def register_checkers(linter):
    """Register checkers."""
    linter.register_checker(ModelChecker(linter))
    linter.register_checker(DjangoInstalledChecker(linter))