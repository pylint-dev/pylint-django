"""Checkers."""
from pylint_django.checkers.auth_user import AuthUserChecker
from pylint_django.checkers.django_installed import DjangoInstalledChecker
from pylint_django.checkers.foreign_key_strings import ForeignKeyStringsChecker
from pylint_django.checkers.forms import FormChecker
from pylint_django.checkers.json_response import JsonResponseChecker
from pylint_django.checkers.models import ModelChecker
from pylint_django.checkers.modelfilter_forloop import\
    ModelFilterForLoopChecker
from pylint_django.checkers.modelsave_forloop import ModelSaveForLoopChecker
from pylint_django.checkers.queryset_iterator import \
    QuerysetIteratorForLoopChecker


def register_checkers(linter):
    """Register checkers."""
    linter.register_checker(ModelChecker(linter))
    linter.register_checker(DjangoInstalledChecker(linter))
    linter.register_checker(JsonResponseChecker(linter))
    linter.register_checker(FormChecker(linter))
    linter.register_checker(AuthUserChecker(linter))
    linter.register_checker(ForeignKeyStringsChecker(linter))
    linter.register_checker(ModelSaveForLoopChecker(linter))
    linter.register_checker(ModelFilterForLoopChecker(linter))
    linter.register_checker(QuerysetIteratorForLoopChecker(linter))
