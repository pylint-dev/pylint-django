import astroid
from pylint.checkers import BaseChecker

from pylint_django.__pkginfo__ import BASE_ID
from pylint_django.compat import check_messages
from pylint_django.transforms import foreignkey


class ForeignKeyStringsChecker(BaseChecker):
    """
    Adds transforms to be able to do type inference for model ForeignKeyField
    properties which use a string to name the foreign relationship. This uses
    Django's model name resolution and this checker wraps the setup to ensure
    Django is able to configure itself before attempting to use the lookups.
    """

    _LONG_MESSAGE = """Finding foreign-key relationships from strings in pylint-django requires configuring Django.
This can be done via the DJANGO_SETTINGS_MODULE environment variable or the pylint option django-settings-module, eg:

    `pylint --load-plugins=pylint_django --django-settings-module=myproject.settings`

. This can also be set as an option in a .pylintrc configuration file.

Some basic default settings were used, however this will lead to less accurate linting.
Consider passing in an explicit Django configuration file to match your project to improve accuracy."""

    name = "Django foreign keys referenced by strings"

    options = (
        (
            "django-settings-module",
            {
                "default": None,
                "type": "string",
                "metavar": "<django settings module>",
                "help": "A module containing Django settings to be used while linting.",
            },
        ),
    )

    msgs = {
        # pylint: disable=implicit-str-concat
        f"E{BASE_ID}10": (
            "Django was not configured. For more information run "
            "pylint --load-plugins=pylint_django --help-msg=django-not-configured",
            "django-not-configured",
            _LONG_MESSAGE,
        ),
        f"F{BASE_ID}10": (
            "Provided Django settings %s could not be loaded",
            "django-settings-module-not-found",
            "The provided Django settings module %s was not found on the path",
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._raise_warning = False

    def open(self):
        # This is a bit of a hacky workaround. pylint-django does not *require* that
        # Django is configured explicitly, and will use some basic defaults in that
        # case. However, as this is a WARNING not a FATAL, the error must be raised
        # with an AST node - only F and R messages are scope exempt (see
        # https://github.com/pylint-dev/pylint/blob/master/pylint/constants.py#L24)

        # However, testing to see if Django is configured happens in `open()`
        # before any modules are inspected, as Django needs to be configured with
        # defaults before the foreignkey checker can work properly. At this point,
        # there are no nodes.

        # Therefore, during the initialisation in `open()`, if django was configured
        # using defaults by pylint-django, it cannot raise the warning yet and
        # must wait until some module is inspected to be able to raise... so that
        # state is stashed in this property.

        try:
            from django.core.exceptions import ImproperlyConfigured  # pylint: disable=import-outside-toplevel
        except ModuleNotFoundError:
            return

        try:
            import django  # pylint: disable=import-outside-toplevel

            django.setup()
            # pylint: disable-next=import-outside-toplevel,unused-import
            from django.apps import apps  # noqa: F401

        except ImproperlyConfigured:
            # this means that Django wasn't able to configure itself using some defaults
            # provided (likely in a DJANGO_SETTINGS_MODULE environment variable)
            # so see if the user has specified a pylint option
            if hasattr(self, "linter"):
                django_settings_module = self.linter.config.django_settings_module
            else:
                # TODO: remove this no-member ignore : this is to avoid the missing `config` for pylint 3+,
                #  and can be removed once pylint 2
                # pylint: disable=no-member
                django_settings_module = self.linter.config.django_settings_module

            if django_settings_module is None:
                # we will warn the user that they haven't actually configured Django themselves
                self._raise_warning = True
                # but use django defaults then...
                from django.conf import settings  # pylint: disable=import-outside-toplevel

                settings.configure()
                django.setup()
            else:
                # see if we can load the provided settings module
                try:
                    from django.conf import Settings, settings  # pylint: disable=import-outside-toplevel

                    settings.configure(Settings(django_settings_module))
                    django.setup()
                except ImportError:
                    # we could not find the provided settings module...
                    # at least here it is a fatal error so we can just raise this immediately
                    self.add_message(
                        "django-settings-module-not-found",
                        args=self.linter.config.django_settings_module,
                    )
                    # however we'll trundle on with basic settings
                    from django.conf import settings  # pylint: disable=import-outside-toplevel

                    settings.configure()
                    django.setup()

        # Now we can add the transforms specific to this checker
        foreignkey.add_transform(astroid.MANAGER)

        # TODO: this is a bit messy having so many inline imports but in order to avoid
        # duplicating the django_installed checker, it'll do for now. In the future, merging
        # those two checkers together might make sense.

    @check_messages("django-not-configured")
    def visit_module(self, node):
        if self._raise_warning:
            # just add it to the first node we see... which isn't nice but not sure what else to do
            self.add_message("django-not-configured", node=node)
            self._raise_warning = False  # only raise it once...
