"""Transforms."""
import os
import re

import astroid

from pylint_django.transforms import foreignkey, fields


foreignkey.add_transform(astroid.MANAGER)
fields.add_transforms(astroid.MANAGER)


def _add_transform(package_name):
    def fake_module_builder():
        """
            Build a fake module to use within transformations.
            @package_name is a parameter from the outher scope b/c according to
            the docs this can't receive any parameters.
            http://pylint.pycqa.org/projects/astroid/en/latest/extending.html?highlight=MANAGER#module-extender-transforms
        """
        transforms_dir = os.path.join(os.path.dirname(__file__), 'transforms')
        fake_module_path = os.path.join(transforms_dir, '%s.py' % re.sub(r'\.', '_', package_name))

        with open(fake_module_path) as modulefile:
            fake_module = modulefile.read()

        return astroid.builder.AstroidBuilder(astroid.MANAGER).string_build(fake_module)

    astroid.register_module_extender(astroid.MANAGER, package_name, fake_module_builder)


_add_transform('django.utils.translation')
# register transform for FileField/ImageField, see #60
_add_transform('django.db.models.fields.files')
