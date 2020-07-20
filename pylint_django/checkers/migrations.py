# Copyright (c) 2018, 2020 Alexander Todorov <atodorov@MrSenko.com>
# Copyright (c) 2020 Bryan Mutai <mutaiwork@gmail.com>

# Licensed under the GPL 2.0: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint-django/blob/master/LICENSE
"""
Various suggestions around migrations. Disabled by default! Enable with
pylint --load-plugins=pylint_django.checkers.migrations
"""

import astroid

from pylint import interfaces
from pylint import checkers
from pylint.checkers import utils

from pylint_plugin_utils import suppress_message

from pylint_django.__pkginfo__ import BASE_ID
from pylint_django import compat
from pylint_django.utils import is_migrations_module


def _is_addfield_with_default(call):
    if not isinstance(call.func, astroid.Attribute):
        return False

    if not call.func.attrname == 'AddField':
        return False

    for keyword in call.keywords:
        # looking for AddField(..., field=XXX(..., default=Y, ...), ...)
        if keyword.arg == 'field' and isinstance(keyword.value, astroid.Call):
            # loop over XXX's keywords
            # NOTE: not checking if XXX is an actual field type because there could
            # be many types we're not aware of. Also the migration will probably break
            # if XXX doesn't instantiate a field object!
            for field_keyword in keyword.value.keywords:
                if field_keyword.arg == 'default':
                    return True

    return False


class NewDbFieldWithDefaultChecker(checkers.BaseChecker):
    """
    Looks for migrations which add new model fields and these fields have a
    default value. According to Django docs this may have performance penalties
    especially on large tables:
    https://docs.djangoproject.com/en/2.0/topics/migrations/#postgresql

    The prefered way is to add a new DB column with null=True because it will
    be created instantly and then possibly populate the table with the
    desired default values.
    """

    __implements__ = (interfaces.IAstroidChecker,)

    # configuration section name
    name = 'new-db-field-with-default'
    msgs = {'W%s98' % BASE_ID: ("%s AddField with default value",
                                'new-db-field-with-default',
                                'Used when Pylint detects migrations adding new '
                                'fields with a default value.')}

    _migration_modules = []
    _possible_offences = {}

    def visit_module(self, node):
        if is_migrations_module(node):
            self._migration_modules.append(node)

    def visit_call(self, node):
        try:
            module = node.frame().parent
        except:  # noqa: E722, pylint: disable=bare-except
            return

        if not is_migrations_module(module):
            return

        if _is_addfield_with_default(node):
            if module not in self._possible_offences:
                self._possible_offences[module] = []

            if node not in self._possible_offences[module]:
                self._possible_offences[module].append(node)

    @utils.check_messages('new-db-field-with-default')
    def close(self):
        def _path(node):
            return node.path

        # sort all migrations by name in reverse order b/c
        # we need only the latest ones
        self._migration_modules.sort(key=_path, reverse=True)

        # filter out the last migration modules under each distinct
        # migrations directory, iow leave only the latest migrations
        # for each application
        last_name_space = ''
        latest_migrations = []
        for module in self._migration_modules:
            name_space = module.path[0].split('migrations')[0]
            if name_space != last_name_space:
                last_name_space = name_space
                latest_migrations.append(module)

        for module, nodes in self._possible_offences.items():
            if module in latest_migrations:
                for node in nodes:
                    self.add_message('new-db-field-with-default', args=module.name, node=node)


class MissingBackwardsMigrationChecker(checkers.BaseChecker):
    __implements__ = (interfaces.IAstroidChecker,)

    name = 'missing-backwards-migration-callable'

    msgs = {'W%s97' % BASE_ID: ('%s Always include backwards migration callable',
                                'missing-backwards-migration-callable',
                                'Always include a backwards/reverse callable counterpart'
                                ' so that the migration is not irreversable.')}

    @utils.check_messages('missing-backwards-migration-callable')
    def visit_call(self, node):
        try:
            module = node.frame().parent
        except:  # noqa: E722, pylint: disable=bare-except
            return

        if not is_migrations_module(module):
            return

        if node.func.as_string().endswith('RunPython') and len(node.args) < 2:
            if node.keywords:
                for keyword in node.keywords:
                    if keyword.arg == 'reverse_code':
                        return
                self.add_message('missing-backwards-migration-callable',
                                 args=module.name, node=node)
            else:
                self.add_message('missing-backwards-migration-callable',
                                 args=module.name, node=node)


def is_in_migrations(node):
    """
        RunPython() migrations receive forward/backwards functions with signature:

            def func(apps, schema_editor):

        which could be unused. This augmentation will suppress all 'unused-argument'
        messages coming from functions in migration modules.
    """
    return is_migrations_module(node.parent)


def load_configuration(linter):
    # don't blacklist migrations for this checker
    new_black_list = list(linter.config.black_list)
    if 'migrations' in new_black_list:
        new_black_list.remove('migrations')
    linter.config.black_list = new_black_list


def register(linter):
    """Required method to auto register this checker."""
    linter.register_checker(NewDbFieldWithDefaultChecker(linter))
    linter.register_checker(MissingBackwardsMigrationChecker(linter))
    if not compat.LOAD_CONFIGURATION_SUPPORTED:
        load_configuration(linter)

    # apply augmentations for migration checkers
    # Unused arguments for migrations
    suppress_message(linter, checkers.variables.VariablesChecker.leave_functiondef,
                     'unused-argument', is_in_migrations)
