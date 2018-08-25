"""
Checks that Pylint does not complain about no self argument in
factory.post_generation method.
"""
#  pylint: disable=missing-docstring,too-few-public-methods,unused-argument,no-member
import factory


class SomeModelFactory(factory.Factory):
    class Meta:
        pass

    @factory.post_generation
    def action(obj, create, extracted, **kwargs):
        if extracted:
            obj.do_action()
        obj.save()
