"""Common Django module."""
from pylint.checkers.base import NameChecker
from pylint_django.augmentations import apply_augmentations
from pylint_plugin_utils import get_checker
import re
from pylint_django.checkers import register_checkers

# we want to import the transforms to make sure they get added to the astroid manager,
# however we don't actually access them directly, so we'll disable the warning
from pylint_django import transforms  # pylint:disable=W0611


def register(linter):
    """Registering additional checkers.

    However, we will also use it to amend existing checker config.
    """
    name_checker = get_checker(linter, NameChecker)
    name_checker.config.good_names += ('qs', 'urlpatterns', 'register', 'app_name',
        'handler500')

    # we don't care about South migrations
    linter.config.black_list += ('migrations', 'south_migrations')

    # add all of the checkers
    register_checkers(linter)

    # register any checking fiddlers
    apply_augmentations(linter)
