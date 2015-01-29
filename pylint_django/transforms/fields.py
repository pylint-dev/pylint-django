from astroid import MANAGER, scoped_nodes, nodes, inference_tip


_STR_FIELDS = ('CharField', 'SlugField', 'URLField', 'TextField', 'EmailField',
               'CommaSeparatedIntegerField', 'FilePathField', 'GenericIPAddressField',
               'IPAddressField', 'RegexField', 'SlugField')
_INT_FIELDS = ('IntegerField', 'SmallIntegerField', 'BigIntegerField',
               'PositiveIntegerField', 'PositiveSmallIntegerField')
_BOOL_FIELDS = ('BooleanField', 'NullBooleanField')


def is_model_field(cls):
    return cls.qname().startswith('django.db.models.fields')


def is_form_field(cls):
    return cls.qname().startswith('django.forms.fields')


def is_model_or_form_field(cls):
    return is_model_field(cls) or is_form_field(cls)


def apply_type_shim(cls, context=None):

    if cls.name in _STR_FIELDS:
        base_node = scoped_nodes.builtin_lookup('str')
    elif cls.name in _INT_FIELDS:
        base_node = scoped_nodes.builtin_lookup('int')
    elif cls.name in _BOOL_FIELDS:
        base_node = scoped_nodes.builtin_lookup('bool')
    elif cls.name == 'FloatField':
        base_node = scoped_nodes.builtin_lookup('float')
    elif cls.name == 'DecimalField':
        base_node = MANAGER.ast_from_module_name('decimal').lookup('Decimal')
    elif cls.name in ('SplitDateTimeField', 'DateTimeField'):
        base_node = MANAGER.ast_from_module_name('datetime').lookup('datetime')
    elif cls.name == 'TimeField':
        base_node = MANAGER.ast_from_module_name('datetime').lookup('time')
    elif cls.name == 'DateField':
        base_node = MANAGER.ast_from_module_name('datetime').lookup('date')
    elif cls.name == 'ManyToManyField':
        base_node = MANAGER.ast_from_module_name('django.db.models.query').lookup('QuerySet')
    elif cls.name in ('ImageField', 'FileField'):
        base_node = MANAGER.ast_from_module_name('django.core.files.base').lookup('File')
    else:
        return iter([cls])

    return iter([cls] + base_node[1])


def add_transforms(manager):
    manager.register_transform(nodes.Class, inference_tip(apply_type_shim), is_model_or_form_field)
