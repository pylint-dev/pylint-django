"""Common Django module."""
from pylint.checkers.base import NameChecker
from pylint_plugin_utils import get_checker

from pylint_django.checkers import register_checkers

# we want to import the transforms to make sure they get added to the astroid manager,
# however we don't actually access them directly, so we'll disable the warning
from pylint_django import transforms  # noqa, pylint: disable=unused-import


def register(linter):
    """
    Registering additional checkers.

    However, we will also use it to amend existing checker config.
    """
    name_checker = get_checker(linter, NameChecker)
    name_checker.config.good_names += ('qs', 'urlpatterns', 'register', 'app_name', 'handler500')

    # we don't care about South migrations
    linter.config.black_list += ('migrations', 'south_migrations')

    # add all of the checkers
    register_checkers(linter)

    # register any checking fiddlers
    try:
        from pylint_django.augmentations import apply_augmentations
        apply_augmentations(linter)
    except ImportError:
        # probably trying to execute pylint_django when Django isn't installed
        # in this case the django-not-installed checker will kick-in
        pass
