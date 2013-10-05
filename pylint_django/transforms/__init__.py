from astroid import MANAGER
from astroid.builder import AstroidBuilder
from astroid import nodes

MODULE_TRANSFORMS = {}


def transform(module):
    try:
        tr = MODULE_TRANSFORMS[module.name]
    except KeyError:
        pass
    else:
        tr(module)
MANAGER.register_transform(nodes.Module, transform)


def class_view_transform(module):
    # all django Views have the value of 'request', 'args' and 'kwargs' set in View.as_view()

    fake = AstroidBuilder(MANAGER).string_build('''
class View(object):
    request = None
    args = None
    kwargs = None

    # as_view is marked as class-only
    def as_view():
        pass
''')
    module.locals['View'] = fake.locals['View']


def model_transform(module):
    fake = AstroidBuilder(MANAGER).string_build('''
class Model:
    objects = None
    id = None
    DoesNotExist = None
    pk = None
    _meta = None

''')
    module.locals['Model'] = fake.locals['Model']

MODULE_TRANSFORMS['django.views.generic.base'] = class_view_transform
MODULE_TRANSFORMS['django.db.models'] = model_transform