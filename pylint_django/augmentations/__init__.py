"""Augmentations."""
#  pylint: disable=invalid-name
from pylint.checkers.base import DocStringChecker, NameChecker
from pylint.checkers.design_analysis import MisdesignChecker
from pylint.checkers.classes import ClassChecker
from pylint.checkers.newstyle import NewStyleConflictChecker
from pylint.checkers.variables import VariablesChecker
from astroid import InferenceError
from pylint_django.compat import ClassDef, ImportFrom, Attribute, django_version
from astroid.objects import Super
from astroid.scoped_nodes import Class as ScopedClass, Module
from pylint.__pkginfo__ import numversion as PYLINT_VERSION
from pylint.checkers.typecheck import TypeChecker
from pylint_django.utils import node_is_subclass, PY3
from pylint_django.compat import inferred
from pylint_plugin_utils import augment_visit, suppress_message

from django.views.generic.base import View, RedirectView, ContextMixin
from django.views.generic.dates import DateMixin, DayMixin, MonthMixin, WeekMixin, YearMixin
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin, TemplateResponseMixin
from django.views.generic.edit import DeletionMixin, FormMixin, ModelFormMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin


# Note: it would have been nice to import the Manager object from Django and
# get its attributes that way - and this used to be the method - but unfortunately
# there's no guarantee that Django is properly configured at that stage, and importing
# anything from the django.db package causes an ImproperlyConfigured exception.
# Therefore we'll fall back on a hard-coded list of attributes which won't be as accurate,
# but this is not 100% accurate anyway.
MANAGER_ATTRS = {
    'none',
    'all',
    'count',
    'dates',
    'distinct',
    'extra',
    'get',
    'get_or_create',
    'get_queryset',
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
}


QS_ATTRS = {
    'filter',
    'exclude',
    'annotate',
    'order_by',
    'reverse',
    'distinct',
    'values',
    'values_list',
    'dates',
    'datetimes',
    'none',
    'all',
    'select_related',
    'prefetch_related',
    'extra',
    'defer',
    'only',
    'using',
    'select_for_update',
    'raw',
    'get',
    'create',
    'get_or_create',
    'update_or_create',
    'bulk_create',
    'count',
    'in_bulk',
    'iterator',
    'latest',
    'earliest',
    'first',
    'last',
    'aggregate',
    'exists',
    'update',
    'delete',
    'as_manager',
    'expression',
    'output_field',
}


MODELADMIN_ATTRS = {
    # options
    'actions',
    'actions_on_top',
    'actions_on_bottom',
    'actions_selection_counter',
    'date_hierarchy',
    'empty_value_display',
    'exclude',
    'fields',
    'fieldsets',
    'filter_horizontal',
    'filter_vertical',
    'form',
    'formfield_overrides',
    'inlines',
    'list_display',
    'list_display_links',
    'list_editable',
    'list_filter',
    'list_max_show_all',
    'list_per_page',
    'list_select_related',
    'ordering',
    'paginator',
    'prepopulated_fields',
    'preserve_filters',
    'radio_fields',
    'raw_id_fields',
    'readonly_fields',
    'save_as',
    'save_on_top',
    'search_fields',
    'show_full_result_count',
    'view_on_site',
    # template options
    'add_form_template',
    'change_form_template',
    'change_list_template',
    'delete_confirmation_template',
    'delete_selected_confirmation_template',
    'object_history_template',
}


MODEL_ATTRS = {
    'DoesNotExist',
    'MultipleObjectsReturned',
    '_base_manager',
    '_default_manager',
    '_meta',
    'delete',
    'get_next_by_date',
    'get_previous_by_date',
    'objects',
    'save',
}


FIELD_ATTRS = {
    'null',
    'blank',
    'choices',
    'db_column',
    'db_index',
    'db_tablespace',
    'default',
    'editable',
    'error_messages',
    'help_text',
    'primary_key',
    'unique',
    'unique_for_date',
    'unique_for_month',
    'unique_for_year',
    'verbose_name',
    'validators',
}


CHAR_FIELD_ATTRS = {
    'max_length',
}


DATE_FIELD_ATTRS = {
    'auto_now',
    'auto_now_add',
}


DECIMAL_FIELD_ATTRS = {
    'max_digits',
    'decimal_places',
}


FILE_FIELD_ATTRS = {
    'upload_to',
    'storage',
}


IMAGE_FIELD_ATTRS = {
    'height_field',
    'width_field',
}


IP_FIELD_ATTRS = {
    'protocol',
    'unpack_ipv4',
}


SLUG_FIELD_ATTRS = {
    'allow_unicode',
}


FOREIGNKEY_FIELD_ATTRS = {
    'limit_choices_to',
    'related_name',
    'related_query_name',
    'to_field',
    'db_constraint',
    'swappable',
}


MANYTOMANY_FIELD_ATTRS = {
    'related_name',
    'related_query_name',
    'limit_choices_to',
    'symmetrical',
    'through',
    'through_fields',
    'db_table',
    'db_constraint',
    'swappable',
}


ONETOONE_FIELD_ATTRS = {
    'parent_link',
}


VIEW_ATTRS = {
    (
        (
            '{}.{}'.format(cls.__module__, cls.__name__),
            '.{}'.format(cls.__name__)
        ),
        tuple(cls.__dict__.keys())
    ) for cls in (
        View, RedirectView, ContextMixin,
        DateMixin, DayMixin, MonthMixin, WeekMixin, YearMixin,
        SingleObjectMixin, SingleObjectTemplateResponseMixin, TemplateResponseMixin,
        DeletionMixin, FormMixin, ModelFormMixin,
        MultipleObjectMixin, MultipleObjectTemplateResponseMixin,
    )
}


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
        if isinstance(stmts[0], ImportFrom):
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

    if node.attrname in MANAGER_ATTRS or node.attrname.endswith('_set'):
        # if this is a X_set method, that's a pretty strong signal that this is the default
        # Django name, rather than one set by related_name
        quack = True
    else:
        # we will
        if isinstance(node.parent, Attribute):
            func_name = getattr(node.parent, 'attrname', None)
            if func_name in MANAGER_ATTRS:
                quack = True

    if quack:
        children = list(node.get_children())
        for child in children:
            try:
                inferred_cls = inferred(child)()
            except InferenceError:
                pass
            else:
                for cls in inferred_cls:
                    if (node_is_subclass(cls,
                                         'django.db.models.manager.Manager',
                                         'django.db.models.base.Model',
                                         '.Model',
                                         'django.db.models.fields.related.ForeignObject')):
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
    if node.name[-5:] != 'Admin' or isinstance(node.parent, ClassDef):
        return False

    return node_is_subclass(node, 'django.contrib.admin.options.ModelAdmin')


def is_model_media_subclass(node):
    """Checks that node is derivative of Media class."""
    if node.name != 'Media' or not isinstance(node.parent, ClassDef):
        return False

    parents = ('django.contrib.admin.options.ModelAdmin',
               'django.forms.widgets.Media',
               'django.db.models.base.Model',
               '.Model',  # for the transformed version used in this plugin
               'django.forms.forms.Form',
               '.Form',
               'django.forms.widgets.Widget',
               '.Widget',
               'django.forms.models.ModelForm',
               '.ModelForm')
    return node_is_subclass(node.parent, *parents)


def is_model_meta_subclass(node):
    """Checks that node is derivative of Meta class."""
    if node.name != 'Meta' or not isinstance(node.parent, ClassDef):
        return False

    parents = ('.Model',  # for the transformed version used here
               'django.db.models.base.Model',
               '.Form',
               'django.forms.forms.Form',
               '.ModelForm',
               'django.forms.models.ModelForm',
               'rest_framework.serializers.BaseSerializer',
               'rest_framework.generics.GenericAPIView',
               'rest_framework.viewsets.ReadOnlyModelViewSet',
               'rest_framework.viewsets.ModelViewSet',
               'django_filters.filterset.FilterSet',)
    return node_is_subclass(node.parent, *parents)


def is_model_factory_meta_subclass(node):
    """Checks that node is derivative of DjangoModelFactory class."""
    if node.name != 'Meta' or not isinstance(node.parent, ClassDef):
        return False

    parents = ('factory.django.DjangoModelFactory',
               '.DjangoModelFactory',)
    return node_is_subclass(node.parent, *parents)


def is_model_mpttmeta_subclass(node):
    """Checks that node is derivative of MPTTMeta class."""
    if node.name != 'MPTTMeta' or not isinstance(node.parent, ClassDef):
        return False

    parents = ('django.db.models.base.Model',
               '.Model',  # for the transformed version used in this plugin
               'django.forms.forms.Form',
               '.Form',
               'django.forms.models.ModelForm',
               '.ModelForm')
    return node_is_subclass(node.parent, *parents)


def _attribute_is_magic(node, attrs, parents):
    """Checks that node is an attribute used inside one of allowed parents"""
    if node.attrname not in attrs:
        return False
    if not node.last_child():
        return False

    try:
        for cls in inferred(node.last_child())():
            if isinstance(cls, Super):
                cls = cls._self_class
            if node_is_subclass(cls, *parents) or cls.qname() in parents:
                return True
    except InferenceError:
        pass
    return False


def is_manager_attribute(node):
    """Checks that node is attribute of Manager or QuerySet class."""
    parents = ('django.db.models.manager.Manager',
               '.Manager',
               'django.db.models.query.QuerySet',
               '.QuerySet')
    return _attribute_is_magic(node, MANAGER_ATTRS.union(QS_ATTRS), parents)


def is_admin_attribute(node):
    """Checks that node is attribute of BaseModelAdmin."""
    parents = ('django.contrib.admin.options.BaseModelAdmin',
               '.BaseModelAdmin')
    return _attribute_is_magic(node, MODELADMIN_ATTRS, parents)


def is_model_attribute(node):
    """Checks that node is attribute of Model."""
    parents = ('django.db.models.base.Model',
               '.Model')
    return _attribute_is_magic(node, MODEL_ATTRS, parents)


def is_field_attribute(node):
    """Checks that node is attribute of Field."""
    parents = ('django.db.models.fields.Field',
               '.Field')
    return _attribute_is_magic(node, FIELD_ATTRS, parents)


def is_charfield_attribute(node):
    """Checks that node is attribute of CharField."""
    parents = ('django.db.models.fields.CharField',
               '.CharField')
    return _attribute_is_magic(node, CHAR_FIELD_ATTRS, parents)


def is_datefield_attribute(node):
    """Checks that node is attribute of DateField."""
    parents = ('django.db.models.fields.DateField',
               '.DateField')
    return _attribute_is_magic(node, DATE_FIELD_ATTRS, parents)


def is_decimalfield_attribute(node):
    """Checks that node is attribute of DecimalField."""
    parents = ('django.db.models.fields.DecimalField',
               '.DecimalField')
    return _attribute_is_magic(node, DECIMAL_FIELD_ATTRS, parents)


def is_filefield_attribute(node):
    """Checks that node is attribute of FileField."""
    parents = ('django.db.models.fields.files.FileField',
               '.FileField')
    return _attribute_is_magic(node, FILE_FIELD_ATTRS, parents)


def is_imagefield_attribute(node):
    """Checks that node is attribute of ImageField."""
    parents = ('django.db.models.fields.files.ImageField',
               '.ImageField')
    return _attribute_is_magic(node, IMAGE_FIELD_ATTRS, parents)


def is_ipfield_attribute(node):
    """Checks that node is attribute of GenericIPAddressField."""
    parents = ('django.db.models.fields.GenericIPAddressField',
               '.GenericIPAddressField')
    return _attribute_is_magic(node, IP_FIELD_ATTRS, parents)


def is_slugfield_attribute(node):
    """Checks that node is attribute of SlugField."""
    parents = ('django.db.models.fields.SlugField',
               '.SlugField')
    return _attribute_is_magic(node, SLUG_FIELD_ATTRS, parents)


def is_foreignkeyfield_attribute(node):
    """Checks that node is attribute of ForeignKey."""
    parents = ('django.db.models.fields.related.ForeignKey',
               '.ForeignKey')
    return _attribute_is_magic(node, FOREIGNKEY_FIELD_ATTRS, parents)


def is_manytomanyfield_attribute(node):
    """Checks that node is attribute of ManyToManyField."""
    parents = ('django.db.models.fields.related.ManyToManyField',
               '.ManyToManyField')
    return _attribute_is_magic(node, MANYTOMANY_FIELD_ATTRS, parents)


def is_onetoonefield_attribute(node):
    """Checks that node is attribute of OneToOneField."""
    parents = ('django.db.models.fields.related.OneToOneField',
               '.OneToOneField')
    return _attribute_is_magic(node, ONETOONE_FIELD_ATTRS, parents)


def is_model_test_case_subclass(node):
    """Checks that node is derivative of TestCase class."""
    if not node.name.endswith('Test') and not isinstance(node.parent, ClassDef):
        return False

    return node_is_subclass(node, 'django.test.testcases.TestCase')


def generic_is_view_attribute(parents, attrs):
    """Generates is_X_attribute function for given parents and attrs."""
    def is_attribute(node):
        return _attribute_is_magic(node, attrs, parents)
    return is_attribute


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
            for cls in inferred(node.last_child())():
                if node_is_subclass(cls, 'django.db.models.base.Model', '.Model'):
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
    if node.name not in ('urlpatterns', 'app_name'):
        return False

    parent = node.parent
    while not isinstance(parent, Module):
        parent = parent.parent

    if not parent.name.endswith('urls'):
        return False

    return True


def allow_meta_protected_access(node):
    if django_version >= (1, 8):
        return node.attrname == '_meta'
    else:
        return False


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


def _visit_assign(checker):
    return getattr(checker, 'visit_assign')


def apply_augmentations(linter):
    """Apply augmentation and suppression rules."""
    augment_visit(linter, _visit_attribute(TypeChecker), foreign_key_sets)
    augment_visit(linter, _visit_attribute(TypeChecker), foreign_key_ids)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_model_field_display_method)

    # supress errors when accessing magical class attributes
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_manager_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_admin_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_model_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_field_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_charfield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_datefield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_decimalfield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_filefield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_imagefield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_ipfield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_slugfield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_foreignkeyfield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_manytomanyfield_attribute)
    suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', is_onetoonefield_attribute)

    for parents, attrs in VIEW_ATTRS:
        suppress_message(linter, _visit_attribute(TypeChecker), 'E1101', generic_is_view_attribute(parents, attrs))

    # formviews have too many ancestors, there's nothing the user of the library can do about that
    suppress_message(linter, _visit_class(MisdesignChecker), 'too-many-ancestors', is_class('django.views.generic.edit.FormView'))

    # model forms have no __init__ method anywhere in their bases
    suppress_message(linter, _visit_class(ClassChecker), 'W0232', is_class('django.forms.models.ModelForm'))

    # forms implement __getitem__ but not __len__, thus raising a "Badly implemented container" warning which
    # we will suppress. NOTE: removed from pylint, https://github.com/PyCQA/pylint/issues/112
    # keeping here in case it gets re-implemented
    # suppress_message(linter, _leave_class(MisdesignChecker), 'R0924', is_class('django.forms.forms.Form'))
    # suppress_message(linter, _leave_class(MisdesignChecker), 'R0924', is_class('django.forms.models.ModelForm'))

    # Meta
    suppress_message(linter, _visit_class(DocStringChecker), 'missing-docstring', is_model_meta_subclass)
    suppress_message(linter, _visit_class(NewStyleConflictChecker), 'old-style-class', is_model_meta_subclass)
    suppress_message(linter, _visit_class(ClassChecker), 'no-init', is_model_meta_subclass)
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods', is_model_meta_subclass)
    suppress_message(linter, _visit_attribute(ClassChecker), 'protected-access', allow_meta_protected_access)

    # Media
    suppress_message(linter, _visit_assignname(NameChecker), 'C0103', is_model_media_valid_attributes)
    suppress_message(linter, _visit_class(DocStringChecker), 'missing-docstring', is_model_media_subclass)
    suppress_message(linter, _visit_class(NewStyleConflictChecker), 'old-style-class', is_model_media_subclass)
    suppress_message(linter, _visit_class(ClassChecker), 'no-init', is_model_media_subclass)
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods', is_model_media_subclass)

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

    # factory_boy's DjangoModelFactory
    suppress_message(linter, _visit_class(DocStringChecker), 'missing-docstring', is_model_factory_meta_subclass)
    suppress_message(linter, _visit_class(NewStyleConflictChecker), 'old-style-class', is_model_factory_meta_subclass)
    suppress_message(linter, _visit_class(ClassChecker), 'W0232', is_model_factory_meta_subclass)
    suppress_message(linter, _leave_class(MisdesignChecker), 'too-few-public-methods', is_model_factory_meta_subclass)

    # ForeignKey and OneToOneField
    # Must update this in a thread safe way to support the parallel option on pylint (-j)
    current_leave_module = VariablesChecker.leave_module
    if current_leave_module.__name__ == 'leave_module':
        # current_leave_module is not wrapped
        # Two threads may hit the next assignment concurrently, but the result is the same
        VariablesChecker.leave_module = wrap(current_leave_module, ignore_import_warnings_for_related_fields)
        # VariablesChecker.leave_module is now wrapped
    # else VariablesChecker.leave_module is already wrapped
