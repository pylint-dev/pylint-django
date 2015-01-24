from astroid import MANAGER, scoped_nodes, nodes


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


def make_field_str(cls):
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
    else:
        return cls

    cls.bases.append(base_node[1][0])
    return cls


def add_transforms(manager):
    manager.register_transform(nodes.Class, make_field_str, is_model_field)
    manager.register_transform(nodes.Class, make_field_str, is_form_field)
