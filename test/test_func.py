
import os
import unittest
from django.conf import settings
from pylint.testutils import make_tests, LintTestUsingFile, cb_test_gen, linter


settings.configure()


HERE = os.path.dirname(os.path.abspath(__file__))


linter.load_plugin_modules(['pylint_django'])
linter.global_set_option('required-attributes', ())  # remove required __revision__


def tests():
    callbacks = [cb_test_gen(LintTestUsingFile)]

    input_dir = os.path.join(HERE, 'input')
    messages_dir = os.path.join(HERE, 'messages')

    return make_tests(input_dir, messages_dir, None, callbacks)


def suite():
    return unittest.TestSuite([unittest.makeSuite(test, suiteClass=unittest.TestSuite)
                              for test in tests()])


if __name__=='__main__':
    unittest.main(defaultTest='suite')
