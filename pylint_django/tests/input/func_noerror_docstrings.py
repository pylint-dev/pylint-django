# pylint: disable=missing-class-docstring, missing-module-docstring, too-few-public-methods, missing-function-docstring, no-method-argument, no-self-use, too-many-function-args
class Parent:
    def test():
        return 0

class ChildDoc(Parent):
    def test():
        """Difference"""
        return super().test()
