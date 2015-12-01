"""Augmentations."""
from pylint.checkers.base import DocStringChecker, NameChecker
from pylint.checkers.design_analysis import MisdesignChecker
from pylint.checkers.classes import ClassChecker
from pylint.checkers.newstyle import NewStyleConflictChecker
from pylint.checkers.variables import VariablesChecker
from astroid import InferenceError, Getattr
from astroid.nodes import Class, From
from astroid.scoped_nodes import Class as ScopedClass, Module
from pylint.__pkginfo__ import numversion as PYLINT_VERSION
from pylint.checkers.typecheck import TypeChecker
from pylint_django.utils import node_is_subclass, PY3
from pylint_plugin_utils import augment_visit, suppress_message


def ignore_import_warnings_for_related_fields(orig_method, self, node):
    """
    Replaces the leave_module method on the VariablesChecker class to
    prevent unused-import warnings which are caused by the ForeignKey
    and OneToOneField transformations. By replacing the nodes in the
    AST with their type rather than the django field, imports of the
    form 'from django.db.models import OneToOneField' raise an unused-import
    warning
    """
    to_consume = self._to_consume[0]  # pylint: disable=W0212
    # we can disable this warning ('Access to a protected member _to_consume of a client class')
    # as it's not actually a client class, but rather, this method is being monkey patched
    # onto the class and so the access is valid

    new_things = {}

    iterat = to_consume[0].items if PY3 else to_consume[0].iteritems
    for name, stmts in iterat():
        if isinstance(stmts[0], From):
            if any([n[0] in ('ForeignKey', 'OneToOneField') for n in stmts[0].names]):
                continue
        new_things[name] = stmts

    new_consume = (new_things,) + to_consume[1:]
    self._to_consume = [new_consume]  # pylint: disable=W0212

    return orig_method(self, node)


def foreign_key_sets(chain, node):
    """
    When a Django model has a ForeignKey to another model, the target
    of the foreign key gets a '<modelname>_set' attribute for accessing
    a queryset of the model owning the foreign key - eg:

    class ModelA(models.Model):
        pass

    class ModelB(models.Model):
        a = models.ForeignKey(ModelA)

    Now, ModelA instances will have a modelb_set attribute.

    It's also possible to explicitly name the relationship using the related_name argument
    to the ForeignKey constructor. As it's impossible to know this without inspecting all
    models before processing, we'll instead do a "best guess" approach and see if the attribute
    being accessed goes on to be used as a queryset. This is via 'duck typing': if the method
    called on the attribute being accessed is something we might find in a queryset, we'll
    warn.
    """
    quack = False
    # Note: it would have been nice to import the Manager object from Django and
    # get its attributes that way - and this used to be the method - but unfortunately
    # there's no guarantee that Django is properly configured at that stage, and importing
    # anything from the django.db package causes an ImproperlyConfigured exception.
    # Therefore we'll fall back on a hard-coded list of attributes which won't be as accurate,
    # but this is not 100% accurate anyway.
    manager_attrs = (
        'none',
        'all',
        'count',
        'dates',
        'distinct',
        'extra',
        'get',
        'get_or_create',
        'create',
        'bulk_create',
        'filter',
        'aggregate',
        'annotate',
        'complex_filter',
        'exclude',
        'in_bulk',
        'iterator',
        'latest',
        'order_by',
        'select_for_update',
        'select_related',
        'prefetch_related',
        'values',
        'values_list',
        'update',
        'reverse',
        'defer',
        'only',
        'using',
        'exists',
    )

    if node.attrname in manager_attrs or node.attrname.endswith('_set'):
        # if this is a X_set method, that's a pretty strong signal that this is the default
        # Django name, rather than one set by related_name
        quack = True
    else:
        # we will
        if isinstance(node.parent, Getattr):
            func_name = getattr(node.parent, 'attrname', None)
            if func_name in manager_attrs:
                quack = True

    if quack:
        children = list(node.get_children())
        for child in children:
            try:
                inferred = child.infered()
            except InferenceError:
                pass
            else:
                for cls in inferred:
                    if (node_is_subclass(
                            cls, 'django.db.models.manager.Manager') or
                            node_is_subclass(cls, 'django.db.models.base.Model')):
                        # This means that we are looking at a subclass of models.Model
                        # and something is trying to access a <something>_set attribute.
                        # Since this could exist, we will return so as not to raise an
                        # error.
                        return
    chain()


def foreign_key_ids(chain, node):
    if node.attrname.endswith('_id'):
        return
    chain()


def is_model_admin_subclass(node):
    """Checks that node is derivative of ModelAdmin class."""
    if node.name[-5:] != 'Admin' or isinstance(node.parent, Class):
        return False

    return node_is_subclass(node, 'django.contrib.admin.options.ModelAdmin')


def is_model_media_subclass(node):
    """Checks that node is derivative of Media class."""
    if node.name != 'Media' or not isinstance(node.parent, Class):
        return False

    parents = ('django.contrib.admin.options.ModelAdmin',
               'django.forms.widgets.Media',
               'django.db.models.base.Model',
               'django.forms.forms.Form',
               'django.forms.models.ModelForm')
    return any([node_is_subclass(node.parent, parent) for parent in parents])


def is_model_meta_subclass(node):
    """Checks that node is derivative of Meta class."""
    if node.name != 'Meta' or not isinstance(node.parent, Class):
        return False

    parents = ('django.db.models.base.Model',
               'django.forms.forms.Form',
               'django.forms.models.ModelForm',
               'rest_framework.serializers.ModelSerializer',
               'rest_framework.generics.GenericAPIView',
               'rest_framework.viewsets.ReadOnlyModelViewSet',
               'rest_framework.viewsets.ModelViewSet',
               'django_filters.filterset.FilterSet',)
    return any([node_is_subclass(node.parent, parent) for parent in parents])


def is_model_mpttmeta_subclass(node):
    """Checks that node is derivative of MPTTMeta class."""
    if node.name != 'MPTTMeta' or not isinstance(node.parent, Class):
        return False

    parents = ('django.db.models.base.Model',
               'django.forms.forms.Form',
               'django.forms.models.ModelForm')
    return any([node_is_subclass(node.parent, parent) for parent in parents])


def is_model_test_case_subclass(node):
    """Checks that node is derivative of TestCase class."""
    if not node.name.endswith('Test') and not isinstance(node.parent, Class):
        return False

    return node_is_subclass(node, 'django.test.testcases.TestCase')


def is_model_view_subclass_method_shouldnt_be_function(node):
    """Checks that node is get or post method of the View class."""
    if node.name not in ('get', 'post'):
        return False

    parent = node.parent
    while parent and not isinstance(parent, ScopedClass):
        parent = parent.parent

    subclass = '.View'
    return parent is not None and parent.name.endswith('View') and node_is_subclass(parent, subclass)


def is_model_view_subclass_unused_argument(node):
    """
    Checks that node is get or post method of the View class and it has valid arguments.

    TODO: Bad checkings, need to be more smart.
    """
    if not is_model_view_subclass_method_shouldnt_be_function(node):
        return False

    return 'request' in node.argnames()


def is_model_field_display_method(node):
    """Accept model's fields with get_*_display names."""
    if not node.attrname.endswith('_display'):
        return
    if not node.attrname.startswith('get_'):
        return

    if node.last_child():
        # TODO: could validate the names of the fields on the model rather than
        # blindly accepting get_*_display
        try:
            for cls in node.last_child().infered():
                if node_is_subclass(cls, 'django.db.models.base.Model'):
                    return True
        except InferenceError:
            return False
    return False


def is_model_media_valid_attributes(node):
    """Suppress warnings for valid attributes of Media class."""
    if node.name not in ('js', ):
        return False

    parent = node.parent
    while parent and not isinstance(parent, ScopedClass):
        parent = parent.parent

    if parent is None or parent.name != "Media":
        return False

    return True


def is_templatetags_module_valid_constant(node):
    """Suppress warnings for valid constants in templatetags module."""
    if node.name not in ('register', ):
        return False

    parent = node.parent
    while not isinstance(parent, Module):
        parent = parent.parent

    if "templatetags." not in parent.name:
        return False

    return True


def is_urls_module_valid_constant(node):
    """Suppress warnings for valid constants in urls module."""
    if node.name not in ('urlpatterns', ):
        return False

    parent = node.parent
    while not isinstance(parent, Module):
        parent = parent.parent

    if not parent.name.endswith('urls'):
        return False

    return True


def is_class(class_name):
    """Shortcut for node_is_subclass."""
    return lambda node: node_is_subclass(node, class_name)


def wrap(orig_method, with_method):
    def wrap_func(*args, **kwargs):
        with_method(orig_method, *args, **kwargs)
    return wrap_func


# The names of some visit functions changed in this commit:
# https://bitbucket.org/logilab/pylint/commits/c94ee95abaa5737f13b91626fe321150c0ddd140

def _visit_class(checker):
    return getattr(checker, 'visit_classdef' if PYLINT_VERSION >= (1, 5) else 'visit_class')


def _visit_attribute(checker):
    return getattr(checker, 'visit_attribute' if PYLINT_VERSION >= (1, 5) else 'visit_getattr')


def _leave_class(checker):
    return getattr(checker, 'leave_classdef' if PYLINT_VERSION >= (1, 5) else 'leave_class')


def _leave_function(checker):
    return getattr(checker, 'leave_functiondef' if PYLINT_VERSION >= (1, 5) else 'leave_function')


def _visit_assignname(checker):
    return getattr(checker, 'visit_assignname' if PYLINT_VERSION >= (1, 5) else 'visit_assname')


def apply_augmentations(linter):
    """Apply augmentation and suppression rules."""
    augment_visit(linter, _visit_attribute(TypeChecker), foreign_key_sets)
    augment_visit(linter, _visit_attribute(TypeChecker), foreign_key_ids)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_model_field_display_method)

    # formviews have too many ancestors, there's nothing the user of the library can do about that
    suppress_message(linter, _visit_class(MisdesignChecker), 'R0901', is_class('django.views.generic.edit.FormView'))

    # model forms have no __init__ method anywhere in their bases
    suppress_message(linter, _visit_class(ClassChecker), 'W0232', is_class('django.forms.models.ModelForm'))

    # forms implement __getitem__ but not __len__, thus raising a "Badly implemented container" warning which
    # we will suppress.
    suppress_message(linter, _leave_class(MisdesignChecker), 'R0924', is_class('django.forms.forms.Form'))
    suppress_message(linter, _leave_class(MisdesignChecker), 'R0924', is_class('django.forms.models.ModelForm'))

    # Meta
    suppress_message(linter, _visit_class(DocStringChecker), 'missing-docstring', is_model_meta_subclass)
    suppress_message(linter, _visit_class(NewStyleConflictChecker), 'old-style-class', is_model_meta_subclass)
    suppress_message(linter, _visit_class(ClassChecker), 'no-init', is_model_meta_subclass)
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods', is_model_meta_subclass)

    # Media
    suppress_message(linter, _visit_assignname(NameChecker), 'C0103', is_model_media_valid_attributes)
    suppress_message(linter, _visit_class(DocStringChecker), 'missing-docstring', is_model_media_subclass)
    suppress_message(linter, _visit_class(NewStyleConflictChecker), 'old-style-class', is_model_media_subclass)
    #suppress_message(linter, _visit_class(ClassChecker), 'W0232', is_model_media_subclass)
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods', is_model_media_subclass)

    # Too few public methods started appearing for Views and Models as part of Pylint>=1.4 / astroid>=1.3.3
    # Not sure why, suspect this is a failure to get the parent classes somewhere
    # For now, just suppress it on models and views
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods',
                     is_class('.Model'))
    # TODO: why does this not work with the fqn of 'View'? Must be something to do with the overriding and transforms
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods', is_class('.View'))

    # Admin
    # Too many public methods (40+/20)
    # TODO: Count public methods of django.contrib.admin.options.ModelAdmin and increase
    # MisdesignChecker.config.max_public_methods to this value to count only user' methods.
    #nb_public_methods = 0
    #for method in node.methods():
    #    if not method.name.startswith('_'):
    #        nb_public_methods += 1
    suppress_message(linter, _leave_class(MisdesignChecker), 'R0904', is_model_admin_subclass)

    # Tests
    suppress_message(linter, _leave_class(MisdesignChecker), 'R0904', is_model_test_case_subclass)

    # View
    # Method could be a function (get, post)
    suppress_message(linter, _leave_function(ClassChecker), 'R0201', is_model_view_subclass_method_shouldnt_be_function)
    # Unused argument 'request' (get, post)
    suppress_message(linter, _leave_function(VariablesChecker), 'W0613', is_model_view_subclass_unused_argument)

    # django-mptt
    suppress_message(linter, _visit_class(DocStringChecker), 'missing-docstring', is_model_mpttmeta_subclass)
    suppress_message(linter, _visit_class(NewStyleConflictChecker), 'old-style-class', is_model_mpttmeta_subclass)
    suppress_message(linter, _visit_class(ClassChecker), 'W0232', is_model_mpttmeta_subclass)
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods', is_model_mpttmeta_subclass)

    # ForeignKey and OneToOneField
    VariablesChecker.leave_module = wrap(VariablesChecker.leave_module, ignore_import_warnings_for_related_fields)
