
import os
import sys
import pytest

import pylint

# PYLINT_TEST_FUNCTIONAL_PATH is can be used to force where to pull the classes used for functional testing
# Just make sure you use the exact same version as the one pylint version installed or just add that to PYTHONPATH
pylint_test_func_path = os.getenv('PYLINT_TEST_FUNCTIONAL_PATH', '')
if pylint_test_func_path != '':
    sys.path.append(pylint_test_func_path)

# test_functional has been moved to pylint.testutils as part of the pytlint 2.5 release
# so we try first to load the basic cases and then look in more exotic places
try:
    # pylint <= 2.4 case
    from test_functional import FunctionalTestFile, LintModuleTest  # noqa: E402
except (ImportError, AttributeError):
    try:
        from pylint.testutils import FunctionalTestFile, LintModuleTest
    except (ImportError, AttributeError):
        # test in other more exotic directories
        if os.path.isdir(os.path.join(os.path.dirname(pylint.__file__), 'test')):
            # pre pylint 2.4, pylint was putting files in pylint/test
            sys.path.append(os.path.join(os.path.dirname(pylint.__file__), 'test'))
        elif os.path.isdir(os.path.join(os.path.dirname(pylint.__file__), '..', 'tests')):
            # after version 2.4 pylint moved the test to a 'tests' folder at the root of the github tree
            # to stopped shipping the tests along with the pip package
            # but some distro re-add tests in the packages so only do that when not done at all
            sys.path.append(os.path.join(os.path.dirname(pylint.__file__), '..', 'tests'))
        else:
            # This is a transitional hack specific to pylint 2.4 on travis and should be irrelevant anywhere else
            sys.path.append(os.path.join(os.getenv('HOME', '/home/travis'), 'pylint', 'tests'))
        try:
            from test_functional import FunctionalTestFile, LintModuleTest  # noqa: E402
        except (ImportError, AttributeError):
            from pylint.testutils import FunctionalTestFile, LintModuleTest

# alter sys.path again because the tests now live as a subdirectory
# of pylint_django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
# so we can find migrations
sys.path.append(os.path.join(os.path.dirname(__file__), 'input'))


class PylintDjangoLintModuleTest(LintModuleTest):
    """
        Only used so that we can load this plugin into the linter!
    """
    def __init__(self, test_file):
        super(PylintDjangoLintModuleTest, self).__init__(test_file)
        self._linter.load_plugin_modules(['pylint_django'])
        self._linter.load_plugin_configuration()


class PylintDjangoDbPerformanceTest(PylintDjangoLintModuleTest):
    """
        Only used so that we can load
        pylint_django.checkers.db_performance into the linter!
    """
    def __init__(self, test_file):
        super(PylintDjangoDbPerformanceTest, self).__init__(test_file)
        self._linter.load_plugin_modules(['pylint_django.checkers.db_performance'])
        self._linter.load_plugin_configuration()


def get_tests(input_dir='input', sort=False):
    def _file_name(test):
        return test.base

    HERE = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(HERE, input_dir)

    suite = []
    for fname in os.listdir(input_dir):
        if fname != '__init__.py' and fname.endswith('.py'):
            suite.append(FunctionalTestFile(input_dir, fname))

    # when testing the db_performance plugin we need to sort by input file name
    # because the plugin reports the errors in close() which appends them to the
    # report for the last file in the list
    if sort:
        suite.sort(key=_file_name)

    return suite


TESTS = get_tests()
TESTS.extend(get_tests('input/models'))
TESTS_NAMES = [t.base for t in TESTS]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_everything(test_file):
    # copied from pylint.tests.test_functional.test_functional
    LintTest = PylintDjangoLintModuleTest(test_file)
    LintTest.setUp()
    LintTest._runTest()


# NOTE: define tests for the db_performance checker!
DB_PERFORMANCE_TESTS = get_tests('input/migrations', True)
DB_PERFORMANCE_TESTS_NAMES = [t.base for t in DB_PERFORMANCE_TESTS]


@pytest.mark.parametrize("test_file", DB_PERFORMANCE_TESTS, ids=DB_PERFORMANCE_TESTS_NAMES)
def test_db_performance_plugin(test_file):
    LintTest = PylintDjangoDbPerformanceTest(test_file)
    LintTest.setUp()
    LintTest._runTest()


if __name__ == '__main__':
    sys.exit(pytest.main(sys.argv))
