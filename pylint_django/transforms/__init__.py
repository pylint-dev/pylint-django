import os
import re
from astroid import MANAGER
from astroid.builder import AstroidBuilder
from astroid import nodes


def _add_transform(package_name, *class_names):
    transforms_dir = os.path.join(os.path.dirname(__file__), 'transforms')
    fake_module_path = os.path.join(transforms_dir, '%s.py' % re.sub(r'\.', '_', package_name))

    with open(fake_module_path) as modulefile:
        fake_module = modulefile.read()

    fake = AstroidBuilder(MANAGER).string_build(fake_module)

    def set_fake_locals(module):
        if module.name != package_name:
            return
        for class_name in class_names:
            module.locals[class_name] = fake.locals[class_name]

    MANAGER.register_transform(nodes.Module, set_fake_locals)


_add_transform('django.views.generic.base', 'View')
_add_transform('django.forms', 'Form')
_add_transform('django.forms', 'ModelForm')
_add_transform('django.db.models', 'Model')
_add_transform('django.db.models.fields.files', 'FileField')
_add_transform('django.db.models.fields.files', 'ImageField')
_add_transform('django.db.models.fields.related', 'ManyToManyField')
