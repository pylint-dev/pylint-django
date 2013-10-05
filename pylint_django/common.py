
from pylint.checkers.base import NameChecker
from pylint_django.augmentations import apply_augmentations
from pylint_plugin_utils import get_checker
import re

# we want to import the transforms to make sure they get added to the astroid manager,
# however we don't actually access them directly, so we'll disable the warning
# pylint:disable=W0611
from pylint_django import transforms


def register(linter):
    # this method is meant for registering additional checkers, however
    # we will also use it to amend existing checker config
    name_checker = get_checker(linter, NameChecker)
    name_checker.config.good_names += ('qs',)
    const_rgx = '(%s|urls|urlpatterns|register)' % name_checker.config.const_rgx.pattern
    name_checker.config.const_rgx = re.compile(const_rgx)

    # we don't care about South migrations
    linter.config.black_list += ('migrations',)

    # register any checking fiddlers
    apply_augmentations(linter)
