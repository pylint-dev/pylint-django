"""Augmentations."""
#  pylint: disable=invalid-name
import functools
import itertools

from astroid import InferenceError
from astroid.objects import Super
from astroid.nodes import ClassDef, ImportFrom, Attribute
from astroid.scoped_nodes import ClassDef as ScopedClass, Module

from pylint.checkers.base import DocStringChecker, NameChecker
from pylint.checkers.design_analysis import MisdesignChecker
from pylint.checkers.classes import ClassChecker
from pylint.checkers.newstyle import NewStyleConflictChecker
from pylint.checkers.variables import VariablesChecker
from pylint.checkers.typecheck import TypeChecker
from pylint.checkers.variables import ScopeConsumer

from pylint_plugin_utils import augment_visit, suppress_message

from django import VERSION as django_version
from django.views.generic.base import View, RedirectView, ContextMixin
from django.views.generic.dates import DateMixin, DayMixin, MonthMixin, WeekMixin, YearMixin
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin, TemplateResponseMixin
from django.views.generic.edit import DeletionMixin, FormMixin, ModelFormMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.utils import termcolors

from pylint_django.utils import node_is_subclass, PY3


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
    'id',
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
    'add',
    'clear',
    'related_name',
    'related_query_name',
    'remove',
    'set',
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


STYLE_ATTRS = set(itertools.chain.from_iterable(termcolors.PALETTES.values()))


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


FORM_ATTRS = {
    'declared_fields',
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
    consumer = self._to_consume[0]  # pylint: disable=W0212
    # we can disable this warning ('Access to a protected member _to_consume of a client class')
    # as it's not actually a client class, but rather, this method is being monkey patched
    # onto the class and so the access is valid

    new_things = {}

    iterat = consumer.to_consume.items if PY3 else consumer.to_consume.iteritems
    for name, stmts in iterat():
        if isinstance(stmts[0], ImportFrom):
            if any([n[0] in ('ForeignKey', 'OneToOneField') for n in stmts[0].names]):
                continue
        new_things[name] = stmts

    consumer._atomic = ScopeConsumer(new_things, consumer.consumed, consumer.scope_type)  # pylint: disable=W0212
    self._to_consume = [consumer]  # pylint: disable=W0212

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
                inferred_cls = child.inferred()
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
               'django_filters.filterset.FilterSet',
               'factory.django.DjangoModelFactory',)
    return node_is_subclass(node.parent, *parents)


def is_model_factory(node):
    """Checks that node is derivative of DjangoModelFactory or SubFactory class."""
    try:
        parent_classes = node.expr.inferred()
    except:  # noqa: E722, pylint: disable=bare-except
        return False

    parents = ('factory.declarations.LazyFunction',
               'factory.declarations.SubFactory',
               'factory.django.DjangoModelFactory')

    for parent_class in parent_classes:
        try:
            if parent_class.qname() in parents:
                return True

            if node_is_subclass(parent_class, *parents):
                return True
        except AttributeError:
            continue

    return False


def is_factory_post_generation_method(node):
    if not node.decorators:
        return False

    for decorator in node.decorators.get_children():
        try:
            inferred = decorator.inferred()
        except InferenceError:
            continue

        for target in inferred:
            if target.qname() == 'factory.helpers.post_generation':
                return True

    return False


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
        for cls in node.last_child().inferred():
            if isinstance(cls, Super):
                cls = cls._self_class  # pylint: disable=protected-access
            if node_is_subclass(cls, *parents) or cls.qname() in parents:
                return True
    except InferenceError:
        pass
    return False


def is_style_attribute(node):
    parents = ('django.core.management.color.Style', )
    return _attribute_is_magic(node, STYLE_ATTRS, parents)


def is_manager_attribute(node):
    """Checks that node is attribute of Manager or QuerySet class."""
    parents = ('django.db.models.manager.Manager',
               '.Manager',
               'factory.base.BaseFactory.build',
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


def is_form_attribute(node):
    """Checks that node is attribute of Form."""
    parents = ('django.forms.forms.Form', 'django.forms.models.ModelForm')
    return _attribute_is_magic(node, FORM_ATTRS, parents)


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

    subclass = ('django.views.View',
                'django.views.generic.View',
                'django.views.generic.base.View',)

    return parent is not None and node_is_subclass(parent, *subclass)


def ignore_unused_argument_warnings_for_request(orig_method, self, stmt, name):
    """
    Ignore unused-argument warnings for function arguments named "request".

    The signature of Django view functions require the request argument but it is okay if the request is not used.
    This function should be used as a wrapper for the `VariablesChecker._is_name_ignored` method.
    """
    if name == 'request':
        return True

    return orig_method(self, stmt, name)


def is_model_field_display_method(node):
    """Accept model's fields with get_*_display names."""
    if not node.attrname.endswith('_display'):
        return False
    if not node.attrname.startswith('get_'):
        return False

    if node.last_child():
        # TODO: could validate the names of the fields on the model rather than
        # blindly accepting get_*_display
        try:
            for cls in node.last_child().inferred():
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

    return False


def is_class(class_name):
    """Shortcut for node_is_subclass."""
    return lambda node: node_is_subclass(node, class_name)


def wrap(orig_method, with_method):
    @functools.wraps(orig_method)
    def wrap_func(*args, **kwargs):
        return with_method(orig_method, *args, **kwargs)
    return wrap_func


def is_wsgi_application(node):
    frame = node.frame()
    return node.name == 'application' and isinstance(frame, Module) and \
        (frame.name == 'wsgi' or frame.path[0].endswith('wsgi.py') or frame.file.endswith('wsgi.py'))


# Compat helpers
def pylint_newstyle_classdef_compat(linter, warning_name, augment):
    if not hasattr(NewStyleConflictChecker, 'visit_classdef'):
        return
    suppress_message(linter, getattr(NewStyleConflictChecker, 'visit_classdef'), warning_name, augment)


def apply_wrapped_augmentations():
    """
    Apply augmentation and supression rules through monkey patching of pylint.
    """
    # NOTE: The monkey patching is done with wrap and needs to be done in a thread safe manner to support the
    # parallel option of pylint (-j).
    # This is achieved by comparing __name__ of the monkey patched object to the original value and only patch it if
    # these are equal.

    # Unused argument 'request' (get, post)
    current_is_name_ignored = VariablesChecker._is_name_ignored  # pylint: disable=protected-access
    if current_is_name_ignored.__name__ == '_is_name_ignored':
        # pylint: disable=protected-access
        VariablesChecker._is_name_ignored = wrap(current_is_name_ignored, ignore_unused_argument_warnings_for_request)

    # ForeignKey and OneToOneField
    current_leave_module = VariablesChecker.leave_module
    if current_leave_module.__name__ == 'leave_module':
        # current_leave_module is not wrapped
        # Two threads may hit the next assignment concurrently, but the result is the same
        VariablesChecker.leave_module = wrap(current_leave_module, ignore_import_warnings_for_related_fields)
        # VariablesChecker.leave_module is now wrapped
    # else VariablesChecker.leave_module is already wrapped


# augment things
def apply_augmentations(linter):
    """Apply augmentation and suppression rules."""
    augment_visit(linter, TypeChecker.visit_attribute, foreign_key_sets)
    augment_visit(linter, TypeChecker.visit_attribute, foreign_key_ids)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_model_field_display_method)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_style_attribute)
    suppress_message(linter, NameChecker.visit_assignname, 'invalid-name', is_urls_module_valid_constant)

    # supress errors when accessing magical class attributes
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_manager_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_admin_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_model_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_field_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_charfield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_datefield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_decimalfield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_filefield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_imagefield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_ipfield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_slugfield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_foreignkeyfield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_manytomanyfield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_onetoonefield_attribute)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_form_attribute)

    for parents, attrs in VIEW_ATTRS:
        suppress_message(linter, TypeChecker.visit_attribute, 'no-member', generic_is_view_attribute(parents, attrs))

    # formviews have too many ancestors, there's nothing the user of the library can do about that
    suppress_message(linter, MisdesignChecker.visit_classdef, 'too-many-ancestors',
                     is_class('django.views.generic.edit.FormView'))

    # class-based generic views just have a longer inheritance chain
    suppress_message(linter, MisdesignChecker.visit_classdef, 'too-many-ancestors',
                     is_class('django.views.generic.detail.BaseDetailView'))
    suppress_message(linter, MisdesignChecker.visit_classdef, 'too-many-ancestors',
                     is_class('django.views.generic.edit.ProcessFormView'))

    # model forms have no __init__ method anywhere in their bases
    suppress_message(linter, ClassChecker.visit_classdef, 'W0232', is_class('django.forms.models.ModelForm'))

    # Meta
    suppress_message(linter, DocStringChecker.visit_classdef, 'missing-docstring', is_model_meta_subclass)
    pylint_newstyle_classdef_compat(linter, 'old-style-class', is_model_meta_subclass)
    suppress_message(linter, ClassChecker.visit_classdef, 'no-init', is_model_meta_subclass)
    suppress_message(linter, MisdesignChecker.leave_classdef, 'too-few-public-methods', is_model_meta_subclass)
    suppress_message(linter, ClassChecker.visit_attribute, 'protected-access', allow_meta_protected_access)

    # Media
    suppress_message(linter, NameChecker.visit_assignname, 'C0103', is_model_media_valid_attributes)
    suppress_message(linter, DocStringChecker.visit_classdef, 'missing-docstring', is_model_media_subclass)
    pylint_newstyle_classdef_compat(linter, 'old-style-class', is_model_media_subclass)
    suppress_message(linter, ClassChecker.visit_classdef, 'no-init', is_model_media_subclass)
    suppress_message(linter, MisdesignChecker.leave_classdef, 'too-few-public-methods', is_model_media_subclass)

    # Admin
    # Too many public methods (40+/20)
    # TODO: Count public methods of django.contrib.admin.options.ModelAdmin and increase
    # MisdesignChecker.config.max_public_methods to this value to count only user' methods.
    # nb_public_methods = 0
    # for method in node.methods():
    #     if not method.name.startswith('_'):
    #         nb_public_methods += 1
    suppress_message(linter, MisdesignChecker.leave_classdef, 'R0904', is_model_admin_subclass)

    # Tests
    suppress_message(linter, MisdesignChecker.leave_classdef, 'R0904', is_model_test_case_subclass)

    # View
    # Method could be a function (get, post)
    suppress_message(linter, ClassChecker.leave_functiondef, 'no-self-use',
                     is_model_view_subclass_method_shouldnt_be_function)

    # django-mptt
    suppress_message(linter, DocStringChecker.visit_classdef, 'missing-docstring', is_model_mpttmeta_subclass)
    pylint_newstyle_classdef_compat(linter, 'old-style-class', is_model_mpttmeta_subclass)
    suppress_message(linter, ClassChecker.visit_classdef, 'W0232', is_model_mpttmeta_subclass)
    suppress_message(linter, MisdesignChecker.leave_classdef, 'too-few-public-methods', is_model_mpttmeta_subclass)

    # factory_boy's DjangoModelFactory
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member', is_model_factory)
    suppress_message(linter, ClassChecker.visit_functiondef, 'no-self-argument', is_factory_post_generation_method)

    # wsgi.py
    suppress_message(linter, NameChecker.visit_assignname, 'invalid-name', is_wsgi_application)

    apply_wrapped_augmentations()
