
import os
import sys
import pytest

import pylint
# because there's no __init__ file in pylint/test/
sys.path.append(os.path.join(os.path.dirname(pylint.__file__), 'test'))
import test_functional

from pylint_django.compat import django_version


class PylintDjangoLintModuleTest(test_functional.LintModuleTest):
    """
        Only used so that we can load this plugin into the linter!
    """
    def __init__(self, test_file):
        super(PylintDjangoLintModuleTest, self).__init__(test_file)
        self._linter.load_plugin_modules(['pylint_django'])


def get_tests():
    HERE = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(HERE, 'input')

    suite = []
    for fname in os.listdir(input_dir):
        if fname != '__init__.py' and fname.endswith('.py'):
            suite.append(test_functional.FunctionalTestFile(input_dir, fname))
    return suite


TESTS = get_tests()
TESTS_NAMES = [t.base for t in TESTS]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_everything(test_file):
    # copied from pylint.tests.test_functional.test_functional
    LintTest = PylintDjangoLintModuleTest(test_file)
    LintTest.setUp()
    LintTest._runTest()


if __name__ == '__main__':
    sys.exit(pytest.main(sys.argv))
