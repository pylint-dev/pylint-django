from astroid import InferenceError
from pylint.checkers.typecheck import TypeChecker
from pylint_plugin_utils import augment_visit


def foreign_key(chain, node):
    """
    Pylint will raise an error when accesing a member of a ForeignKey
    attribute on a Django model. This augmentation supresses this error.
    """
    # TODO: if possible, infer the 'real' type of the foreign key attribute
    # by using the 'to' value given to its constructor
    if node.last_child():
        try:
            for infered in node.last_child().infered():
                if infered.pytype() == 'django.db.models.fields.related.ForeignKey':
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
                    for base_cls in cls.bases:
                        if base_cls.attrname != 'Model':
                            continue
                        try:
                            for inf in base_cls.infered():
                                if inf.qname() == 'django.db.models.base.Model':
                                    # This means that we are looking at a subclass of models.Model
                                    # and something is trying to access a <something>_set attribute.
                                    # Since this could exist, we will return so as not to raise an
                                    # error.
                                    return
                        except InferenceError:
                            pass
    chain()


def apply_augmentations(linter):
    augment_visit(linter, TypeChecker.visit_getattr, foreign_key_sets)
    augment_visit(linter, TypeChecker.visit_getattr, foreign_key)