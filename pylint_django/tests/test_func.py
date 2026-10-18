from __future__ import annotations

import os
import pickle
import sys
from pathlib import Path

import pytest
from _pytest.config import Config
from pylint.testutils import FunctionalTestFile, LintModuleTest
from pylint.testutils.functional import get_functional_test_files_from_directory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pylint_django.tests.settings")

TESTS_DIR = Path(__file__).parent
REPOSITORY_ROOT = TESTS_DIR.parent.parent
# The Django app and models package listed in the test settings
DJANGO_SUPPORT_DIR = TESTS_DIR / "input"
FUNCTIONAL_DIR = TESTS_DIR / "functional"

sys.path += [str(p.absolute()) for p in (TESTS_DIR, REPOSITORY_ROOT, DJANGO_SUPPORT_DIR)]


class PylintDjangoLintModuleTest(LintModuleTest):
    """
    Only used so that we can load this plugin into the linter!
    """

    def __init__(self, test_file: FunctionalTestFile, config: Config | None = None) -> None:
        super().__init__(test_file, config)
        self._linter.load_plugin_modules(["pylint_django"])
        self._linter.load_plugin_configuration()


class PylintDjangoMigrationsTest(PylintDjangoLintModuleTest):
    """
    Only used so that we can load
    pylint_django.checkers.migrations into the linter!
    """

    def __init__(self, test_file: FunctionalTestFile, config: Config | None = None) -> None:
        super().__init__(test_file, config)
        self._linter.load_plugin_modules(["pylint_django.checkers.migrations"])
        self._linter.load_plugin_configuration()


MIGRATIONS_DIR = FUNCTIONAL_DIR / "migrations"
TESTS = [
    test_file
    for test_file in get_functional_test_files_from_directory(FUNCTIONAL_DIR)
    if Path(test_file._directory) != MIGRATIONS_DIR  # pylint: disable=protected-access
]


@pytest.mark.parametrize("test_file", TESTS, ids=lambda x: x.base)
def test_everything(test_file: FunctionalTestFile):
    lint_test = PylintDjangoLintModuleTest(test_file)
    lint_test.setUp()
    lint_test.runTest()


# NOTE: define tests for the migrations checker!
MIGRATIONS_TESTS = get_functional_test_files_from_directory(MIGRATIONS_DIR)


@pytest.mark.parametrize("migration_test_file", MIGRATIONS_TESTS, ids=lambda x: x.base)
def test_migrations_plugin(migration_test_file: FunctionalTestFile) -> None:
    lint_test = PylintDjangoMigrationsTest(migration_test_file)
    lint_test.setUp()
    lint_test.runTest()


@pytest.mark.parametrize("test_file", MIGRATIONS_TESTS[:1], ids=lambda x: x.base)
@pytest.mark.skip  # TODO currently skipped because ArgParser which pylint uses is not pickable.
def test_linter_should_be_pickleable_with_pylint_django_plugin_installed(test_file):
    lint_test = PylintDjangoMigrationsTest(test_file)
    lint_test.setUp()
    # pylint: disable=protected-access
    # LintModuleTest sets reporter to instance of FunctionalTestReporter that is not picklable
    lint_test._linter.reporter = None
    pickle.dumps(lint_test._linter)
