from pylint.checkers.base import DocStringChecker, NameChecker
from pylint.checkers.design_analysis import MisdesignChecker
from pylint.checkers.classes import ClassChecker
from pylint.checkers.newstyle import NewStyleConflictChecker
from pylint.checkers.variables import VariablesChecker
from astroid import InferenceError
from astroid.nodes import Class
from astroid.scoped_nodes import Class as ScopedClass
from pylint.checkers.typecheck import TypeChecker
from pylint_django.utils import node_is_subclass
from pylint_plugin_utils import augment_visit, suppress_message


def related_field_attributes(chain, node):
    """
    Pylint will raise an error when accesing a member of a ForeignKey
    attribute on a Django model. This augmentation supresses this error.
    """
    # TODO: if possible, infer the 'real' type of the foreign key attribute
    # by using the 'to' value given to its constructor
    related_fields = (
        'django.db.models.fields.related.ForeignKey',
        'django.db.models.fields.related.OneToOneField'
        'django.db.models.fields.related.ManyToManyField'
    )
    if node.last_child():
        try:
            for infered in node.last_child().infered():
                if infered.pytype() in related_fields:
                    return
        except InferenceError:
            pass

    chain()


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
    """
    if node.attrname.endswith('_set'):
        children = list(node.get_children())
        for child in children:
            try:
                inferred = child.infered()
            except InferenceError:
                pass
            else:
                for cls in inferred:
                    if node_is_subclass(cls, 'django.db.models.base.Model'):
                        # This means that we are looking at a subclass of models.Model
                        # and something is trying to access a <something>_set attribute.
                        # Since this could exist, we will return so as not to raise an
                        # error.
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
    if node.name != 'Meta' or not isinstance(node.parent, Class):
        return False

    parents = ('django.db.models.base.Model',
               'django.forms.forms.Form',
               'django.forms.models.ModelForm')
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

    #subclass = 'django.views.generic.base.View'
    subclass = '.View'
    return parent.name.endswith('View') and node_is_subclass(parent, subclass)


def is_model_view_subclass_unused_argument(node):
    """Checks that node is get or post method of the View class and it has valid arguments.

    TODO: Bad checkings, need to be more smart.
    """
    if not is_model_view_subclass_method_shouldnt_be_function(node):
        return False

    return 'request' in node.argnames()


def is_model_field_display_method(node):
    if not node.attrname.endswith('_display'):
        return
    if not node.attrname.startswith('get_'):
        return

    if node.last_child():
        # TODO: could validate the names of the fields on the model rather than
        # blindly accepting get_*_display
        for cls in node.last_child().infered():
            if node_is_subclass(cls, 'django.db.models.base.Model'):
                return True
    return False


def is_model_media_valid_attributes(node):
    """Suppress warnings for valid attributes of Media class."""
    if node.name not in ('js', ):
        return False

    parent = node.parent
    while parent and not isinstance(parent, ScopedClass):
        parent = parent.parent

    if parent == None or parent.name != "Media":
        return False

    return True


def is_class(class_name):
    return lambda node: node_is_subclass(node, class_name)


def apply_augmentations(linter):
    augment_visit(linter, TypeChecker.visit_getattr, foreign_key_sets)
    augment_visit(linter, TypeChecker.visit_getattr, related_field_attributes)
    suppress_message(linter, TypeChecker.visit_getattr, 'E1101', is_model_field_display_method)

    # formviews have too many ancestors, there's nothing the user of the library can do about that
    suppress_message(linter, MisdesignChecker.visit_class, 'R0901', is_class('django.views.generic.edit.FormView'))

    # model forms have no __init__ method anywhere in their bases
    suppress_message(linter, ClassChecker.visit_class, 'W0232', is_class('django.forms.models.ModelForm'))

    # forms implement __getitem__ but not __len__, thus raising a "Badly implemented container" warning which
    # we will suppress.
    suppress_message(linter, MisdesignChecker.leave_class, 'R0924', is_class('django.forms.forms.Form'))
    suppress_message(linter, MisdesignChecker.leave_class, 'R0924', is_class('django.forms.models.ModelForm'))

    # Meta
    suppress_message(linter, DocStringChecker.visit_class, 'C0111', is_model_meta_subclass)
    suppress_message(linter, NewStyleConflictChecker.visit_class, 'C1001', is_model_meta_subclass)
    suppress_message(linter, ClassChecker.visit_class, 'W0232', is_model_meta_subclass)
    suppress_message(linter, MisdesignChecker.leave_class, 'R0903', is_model_meta_subclass)

    # Media
    suppress_message(linter, NameChecker.visit_assname, 'C0103', is_model_media_valid_attributes)
    suppress_message(linter, DocStringChecker.visit_class, 'C0111', is_model_media_subclass)
    suppress_message(linter, NewStyleConflictChecker.visit_class, 'C1001', is_model_media_subclass)
    suppress_message(linter, ClassChecker.visit_class, 'W0232', is_model_media_subclass)
    suppress_message(linter, MisdesignChecker.leave_class, 'R0903', is_model_media_subclass)

    # Admin
    # Too many public methods (40+/20)
    # TODO: Count public methods of django.contrib.admin.options.ModelAdmin and increase MisdesignChecker.config.max_public_methods to this value to count only user' methods.
    #nb_public_methods = 0
    #for method in node.methods():
    #    if not method.name.startswith('_'):
    #        nb_public_methods += 1
    suppress_message(linter, MisdesignChecker.leave_class, 'R0904', is_model_admin_subclass)

    # Tests
    suppress_message(linter, MisdesignChecker.leave_class, 'R0904', is_model_test_case_subclass)

    # View
    suppress_message(linter, ClassChecker.leave_function, 'R0201', is_model_view_subclass_method_shouldnt_be_function)  # Method could be a function (get, post)
    suppress_message(linter, VariablesChecker.leave_function, 'W0613', is_model_view_subclass_unused_argument)  # Unused argument 'request' (get, post)

    # django-mptt
    suppress_message(linter, DocStringChecker.visit_class, 'C0111', is_model_mpttmeta_subclass)
    suppress_message(linter, NewStyleConflictChecker.visit_class, 'C1001', is_model_mpttmeta_subclass)
    suppress_message(linter, ClassChecker.visit_class, 'W0232', is_model_mpttmeta_subclass)
    suppress_message(linter, MisdesignChecker.leave_class, 'R0903', is_model_mpttmeta_subclass)
