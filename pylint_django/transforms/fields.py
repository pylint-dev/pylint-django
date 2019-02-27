from astroid import (
    MANAGER, scoped_nodes, nodes, inference_tip,
    AstroidImportError
)

from pylint_django import utils


_STR_FIELDS = ('CharField', 'SlugField', 'URLField', 'TextField', 'EmailField',
               'CommaSeparatedIntegerField', 'FilePathField', 'GenericIPAddressField',
               'IPAddressField', 'RegexField', 'SlugField')
_INT_FIELDS = ('IntegerField', 'SmallIntegerField', 'BigIntegerField',
               'PositiveIntegerField', 'PositiveSmallIntegerField')
_BOOL_FIELDS = ('BooleanField', 'NullBooleanField')
_RANGE_FIELDS = ('RangeField', 'IntegerRangeField', 'BigIntegerRangeField',
                 'FloatRangeField', 'DateTimeRangeField', 'DateRangeField')


def is_model_field(cls):
    return cls.qname().startswith('django.db.models.fields') or \
        cls.qname().startswith('django.contrib.postgres.fields')


def is_form_field(cls):
    return cls.qname().startswith('django.forms.fields')


def is_model_or_form_field(cls):
    return is_model_field(cls) or is_form_field(cls)


def apply_type_shim(cls, _context=None):  # noqa

    if cls.name in _STR_FIELDS:
        base_nodes = scoped_nodes.builtin_lookup('str')
    elif cls.name in _INT_FIELDS:
        base_nodes = scoped_nodes.builtin_lookup('int')
    elif cls.name in _BOOL_FIELDS:
        base_nodes = scoped_nodes.builtin_lookup('bool')
    elif cls.name == 'FloatField':
        base_nodes = scoped_nodes.builtin_lookup('float')
    elif cls.name == 'DecimalField':
        try:
            base_nodes = MANAGER.ast_from_module_name('_decimal').lookup('Decimal')
        except AstroidImportError:
            base_nodes = MANAGER.ast_from_module_name('_pydecimal').lookup('Decimal')
    elif cls.name in ('SplitDateTimeField', 'DateTimeField'):
        base_nodes = MANAGER.ast_from_module_name('datetime').lookup('datetime')
    elif cls.name == 'TimeField':
        base_nodes = MANAGER.ast_from_module_name('datetime').lookup('time')
    elif cls.name == 'DateField':
        base_nodes = MANAGER.ast_from_module_name('datetime').lookup('date')
    elif cls.name == 'DurationField':
        base_nodes = MANAGER.ast_from_module_name('datetime').lookup('timedelta')
    elif cls.name == 'UUIDField':
        base_nodes = MANAGER.ast_from_module_name('uuid').lookup('UUID')
    elif cls.name == 'ManyToManyField':
        base_nodes = MANAGER.ast_from_module_name('django.db.models.query').lookup('QuerySet')
    elif cls.name in ('ImageField', 'FileField'):
        base_nodes = MANAGER.ast_from_module_name('django.core.files.base').lookup('File')
    elif cls.name == 'ArrayField':
        base_nodes = scoped_nodes.builtin_lookup('list')
    elif cls.name in ('HStoreField', 'JSONField'):
        base_nodes = scoped_nodes.builtin_lookup('dict')
    elif cls.name in _RANGE_FIELDS:
        base_nodes = MANAGER.ast_from_module_name('psycopg2._range').lookup('Range')
    else:
        return iter([cls])

    # XXX: for some reason, with python3, this particular line triggers a
    # check in the StdlibChecker for deprecated methods; one of these nodes
    # is an ImportFrom which has no qname() method, causing the checker
    # to die...
    if utils.PY3:
        base_nodes = [n for n in base_nodes[1] if not isinstance(n, nodes.ImportFrom)]
    else:
        base_nodes = list(base_nodes[1])

    return iter([cls] + base_nodes)


def add_transforms(manager):
    manager.register_transform(nodes.ClassDef, inference_tip(apply_type_shim), is_model_or_form_field)
