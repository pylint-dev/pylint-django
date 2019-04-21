
import os
import sys
import pytest

import pylint
# because there's no __init__ file in pylint/test/
sys.path.append(os.path.join(os.path.dirname(pylint.__file__), 'test'))
import test_functional  # noqa: E402

# alter sys.path again because the tests now live as a subdirectory
# of pylint_django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
# so we can find migrations
sys.path.append(os.path.join(os.path.dirname(__file__), 'input'))


class PylintDjangoLintModuleTest(test_functional.LintModuleTest):
    """
        Only used so that we can load this plugin into the linter!
    """
    def __init__(self, test_file):
        super(PylintDjangoLintModuleTest, self).__init__(test_file)
        self._linter.load_plugin_modules(['pylint_django'])


class PylintDjangoDbPerformanceTest(PylintDjangoLintModuleTest):
    """
        Only used so that we can load
        pylint_django.checkers.db_performance into the linter!
    """
    def __init__(self, test_file):
        super(PylintDjangoDbPerformanceTest, self).__init__(test_file)
        self._linter.load_plugin_modules(['pylint_django.checkers.db_performance'])


def get_tests(input_dir='input', sort=False):
    def _file_name(test):
        return test.base

    HERE = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(HERE, input_dir)

    suite = []
    for fname in os.listdir(input_dir):
        if fname != '__init__.py' and fname.endswith('.py'):
            suite.append(test_functional.FunctionalTestFile(input_dir, fname))

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
