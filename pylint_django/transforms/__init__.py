"""
These transforms replace the Django types with adapted versions to provide
additional typing and method inference to pylint. All of these transforms
are considered "global" to pylint-django, in that all checks and improvements
requre them to be loaded. Additional transforms specific to checkers are loaded
by the checker rather than here.

For example, the ForeignKeyStringsChecker loads the foreignkey.py transforms
itself as it may be disabled independently of the rest of pylint-django
"""
import os
import re

import astroid

from pylint_django.transforms import fields

fields.add_transforms(astroid.MANAGER)


def _add_transform(package_name):
    def fake_module_builder():
        """
        Build a fake module to use within transformations.
        @package_name is a parameter from the outer scope b/c according to
        the docs this can't receive any parameters.
        http://pylint.pycqa.org/projects/astroid/en/latest/extending.html?highlight=MANAGER#module-extender-transforms
        """
        transforms_dir = os.path.join(os.path.dirname(__file__), "transforms")
        transformed_name = re.sub(r"\.", "_", package_name)
        fake_module_path = os.path.join(transforms_dir, f"{transformed_name}.py")

        with open(fake_module_path, encoding="utf-8") as modulefile:
            fake_module = modulefile.read()

        return astroid.builder.AstroidBuilder(astroid.MANAGER).string_build(fake_module)

    astroid.register_module_extender(astroid.MANAGER, package_name, fake_module_builder)


_add_transform("django.utils.translation")
# register transform for FileField/ImageField, see #60
_add_transform("django.db.models.fields.files")
