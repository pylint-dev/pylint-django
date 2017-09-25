import re
from os.path import abspath, dirname, join
import sys
import unittest
from django.conf import settings
from pylint.testutils import _get_tests_info, linter
from pylint.test_func import gen_tests
from pylint_django.compat import django_version

INPUT_DIR = join(dirname(abspath(__file__)), 'input')
MSG_DIR = join(dirname(abspath(__file__)), 'messages')
FILTER_RGX = None

settings.configure()

linter.load_plugin_modules(['pylint_django'])
# Disable some things on Python2.6, since we use a different pylint version here
# (1.3 on Python2.6, 1.4+ on later versions)
if sys.version_info < (2, 7):
    linter.global_set_option('required-attributes', ())
    linter.global_set_option('disable', ('E0012',))

def suite():
    test_list = gen_tests(FILTER_RGX)
    return unittest.TestSuite([unittest.makeSuite(test, suiteClass=unittest.TestSuite)
                               for test in test_list])

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
