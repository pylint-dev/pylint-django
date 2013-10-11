
from os.path import join, dirname, abspath
import unittest
from logilab.common import testlib
from pylint.testutils import make_tests, LintTestUsingModule, LintTestUsingFile, cb_test_gen, linter
import sys


INPUT_DIR = join(dirname(abspath(__file__)), 'input')
MESSAGES_DIR = join(dirname(abspath(__file__)), 'messages')
CALLBACKS = [cb_test_gen(LintTestUsingModule), cb_test_gen(LintTestUsingFile)]
FILTER_RGX = None


linter.load_plugin_modules(['pylint_django'])
linter.global_set_option('required-attributes', ()) # remove required __revision__


def suite():
    return testlib.TestSuite([unittest.makeSuite(test, suiteClass=testlib.TestSuite)
                              for test in make_tests(INPUT_DIR, MESSAGES_DIR,
                                                     FILTER_RGX, CALLBACKS)])

if __name__=='__main__':
    if len(sys.argv) > 1:
        FILTER_RGX = sys.argv[1]
        del sys.argv[1]
    testlib.unittest_main(defaultTest='suite')


