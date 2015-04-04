
import os
import unittest
from django.conf import settings
from logilab.common import testlib
from pylint.testutils import make_tests, LintTestUsingFile, cb_test_gen, linter


settings.configure()


HERE = os.path.dirname(os.path.abspath(__file__))


linter.load_plugin_modules(['pylint_django'])
linter.global_set_option('required-attributes', ())  # remove required __revision__

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def tests(input_dir, messages_dir):
    callbacks = [cb_test_gen(LintTestUsingFile)]

    input_dir = os.path.join(HERE, input_dir)
    messages_dir = os.path.join(HERE, messages_dir)

    return make_tests(input_dir, messages_dir, None, callbacks)


def suite():
    test_list = tests('input', 'messages')
    
    if module_exists('rest_framework'):
        test_list += tests('external_drf', '')

    return testlib.TestSuite([unittest.makeSuite(test, suiteClass=testlib.TestSuite)
                              for test in test_list])

if __name__=='__main__':
    testlib.unittest_main(defaultTest='suite')
