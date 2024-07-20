"""Common Django module."""

# we want to import the transforms to make sure they get added to the astroid manager,
# however we don't actually access them directly, so we'll disable the warning
from pylint_django import compat
from pylint_django.checkers import register_checkers


def load_configuration(linter):
    """
    Amend existing checker config.
    """
    linter.config.good_names += (
        "pk",
        "qs",
        "urlpatterns",
        "register",
        "app_name",
        "handler400",
        "handler403",
        "handler404",
        "handler500",
    )

    # we don't care about South migrations
    linter.config.black_list += ("migrations", "south_migrations")


def register(linter):
    """
    Registering additional checkers.
    """
    # add all of the checkers
    register_checkers(linter)

    # register any checking fiddlers
    try:
        # pylint: disable=import-outside-toplevel
        from pylint_django.augmentations import apply_augmentations

        apply_augmentations(linter)
    except ImportError:
        # probably trying to execute pylint_django when Django isn't installed
        # in this case the django-not-installed checker will kick-in
        pass

    if not compat.LOAD_CONFIGURATION_SUPPORTED:
        load_configuration(linter)
