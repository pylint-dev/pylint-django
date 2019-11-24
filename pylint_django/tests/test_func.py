
import os
import sys
import pytest

import pylint


try:
    # pylint 2.5: test_functional has been moved to pylint.testutils
    from pylint.testutils import FunctionalTestFile, LintModuleTest
except (ImportError, AttributeError):
    # specify directly the directory containing test_functional.py
    test_functional_dir = os.getenv('PYLINT_TEST_FUNCTIONAL_DIR', '')

    # otherwise look for in in ~/pylint/tests - pylint 2.4
    # this is the pylint git checkout dir, not the pylint module dir
    if not os.path.isdir(test_functional_dir):
        test_functional_dir = os.path.join(os.getenv('HOME', '/home/travis'), 'pylint', 'tests')

    # or site-packages/pylint/test/ - pylint before 2.4
    if not os.path.isdir(test_functional_dir):
        test_functional_dir = os.path.join(os.path.dirname(pylint.__file__), 'test')

    sys.path.append(test_functional_dir)

    from test_functional import FunctionalTestFile, LintModuleTest


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
