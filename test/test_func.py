
import os
import unittest
from logilab.common import testlib
from pylint.testutils import make_tests, LintTestUsingModule, LintTestUsingFile, cb_test_gen, linter


HERE = os.path.dirname(os.path.abspath(__file__))


linter.load_plugin_modules(['pylint_django'])
linter.global_set_option('required-attributes', ())  # remove required __revision__


def tests():
    callbacks = [cb_test_gen(LintTestUsingModule), cb_test_gen(LintTestUsingFile)]

    input_dir = os.path.join(HERE, 'input')
    messages_dir = os.path.join(HERE, 'messages')

    return make_tests(input_dir, messages_dir, None, callbacks)


def suite():
    return testlib.TestSuite([unittest.makeSuite(test, suiteClass=testlib.TestSuite)
                              for test in tests()])


if __name__=='__main__':
    testlib.unittest_main(defaultTest='suite')
