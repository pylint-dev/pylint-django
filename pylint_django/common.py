from astroid import MANAGER
from astroid.builder import AstroidBuilder
from astroid import nodes
from pylint.checkers.base import NameChecker
import re


def register(linter):
    # this method is meant for registering additional checkers, however
    # we will also use it to amend existing checker config
    for checker in linter.get_checkers():
        if isinstance(checker, NameChecker):
            checker.config.good_names += ('qs',)
            const_rgx = '(%s|urls|urlpatterns|register)' % checker.config.const_rgx.pattern
            checker.config.const_rgx = re.compile(const_rgx)
    # we don't care about South migrations
    linter.config.black_list += ('migrations',)


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


MODULE_TRANSFORMS['django.views.generic.base'] = class_view_transform