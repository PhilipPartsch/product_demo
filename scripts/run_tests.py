"""Run pytest; "no tests collected" counts as success.

The test results are needs (Sphinx-Test-Reports reads the JUnit XML), so the
test run comes first in every build. An empty starter — or a project before
its first test — has no tests yet: pytest then exits with code 5 although
nothing failed, and still writes the JUnit file. This wrapper turns exit
code 5 into 0; every other result (failures, errors) is passed through.

Usage: python scripts/run_tests.py <pytest arguments>
"""

import sys

import pytest

code = pytest.main(sys.argv[1:])
sys.exit(0 if code == pytest.ExitCode.NO_TESTS_COLLECTED else int(code))
