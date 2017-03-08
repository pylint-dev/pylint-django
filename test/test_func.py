
import os
import sys
import unittest
from django.conf import settings
from pylint.testutils import make_tests, LintTestUsingFile, cb_test_gen, linter
from pylint_django.compat import django_version


settings.configure()


HERE = os.path.dirname(os.path.abspath(__file__))


linter.load_plugin_modules(['pylint_django'])
# Disable some things on Python2.6, since we use a different pylint version here
# (1.3 on Python2.6, 1.4+ on later versions)
if sys.version_info < (2, 7):
    linter.global_set_option('required-attributes', ())
    linter.global_set_option('disable', ('E0012',))


SKIP_TESTS_FOR_DJANGO_VERSION = {
    # if the second value is False, skip the test, otherwise run it
    ('func_noerror_protected_meta_access', django_version >= (1, 8)),
    ('func_noerror_uuid_field', django_version >= (1, 8)),
}


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

    # first tests which pass for all Django versions
    tests = make_tests(input_dir, messages_dir, None, callbacks)

    # now skip some tests test for specific versions - for example,
    # _meta access should not work for django<1.8 but should run and
    # pass for django 1.4 - skip the tests which will be checking
    # a piece of functionality in pylint-django that should only
    # in higher versions.
    specific_tests = []
    for test_name, version_range in SKIP_TESTS_FOR_DJANGO_VERSION:
        if not version_range:
            specific_tests.append(test_name)
    filter_rgx = '(%s)' % '|'.join(specific_tests)

    tests += make_tests(os.path.join(input_dir, 'versions'), messages_dir, filter_rgx, callbacks)
    return tests


def suite():
    test_list = tests('input', 'messages')
    
    if module_exists('rest_framework'):
        test_list += tests('external_drf', '')

    if module_exists('psycopg2'):
        test_list += tests('external_psycopg2', '')

    return unittest.TestSuite([unittest.makeSuite(test, suiteClass=unittest.TestSuite)
                               for test in test_list])

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
