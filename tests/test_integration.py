#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import contextlib
import os
import re
from pathlib import Path

import pytest  # type: ignore

from fsttest import run_tests

FIXTURES_DIR = Path(__file__).parent / "fixtures"
assert FIXTURES_DIR.is_dir()


def test_run_with_failures(capfd) -> None:
    """
    Tests running this within the fixtures dir.
    """

    with pytest.raises(SystemExit):
        with cd(FIXTURES_DIR):
            test_dir = Path("test_suite_with_failures")
            assert test_dir.is_dir()
            run_tests(test_dir)

    stdout, stderr = capfd.readouterr()

    assert "No FST test cases found" not in stdout

    # It should tell us that things have failed.
    m = re.search(r"Failed \d+ tests?", stdout)
    assert m, f"Could not find failure message in stdout: {stdout}"

    # Find out how many passed.
    m = re.search(r"[(](\d+)/(\d+)[)] passed", stdout)
    assert m, f"Could not find passed status in stdout: {stdout}"
    assert int(m[1]) < int(m[2]), "Expected to find fewer passed tests."

    # Find formatted error messages.
    assert "test_a_b.toml: Failure" in stderr
    assert "test_rewrite_rules.toml: Failure" in stderr
    assert "Given: 'b'" in stderr
    assert "Expected: 'a'" in stderr

    # Find Foma defines in stderr
    assert re.search(
        r"defined \w+: \d+ bytes?", stderr
    ), "Should find Foma output in failed test run"


def test_run_empty_test_suite(capsys) -> None:
    """
    Tests running this within the fixtures dir.
    """

    with pytest.raises(SystemExit):
        with cd(FIXTURES_DIR):
            test_dir = Path("empty_test_suite")
            assert test_dir.is_dir()
            run_tests(test_dir)

    stdout, stderr = capsys.readouterr()
    assert "No FST test cases found" in stdout


def test_run_successfull_test_suiote(capfd) -> None:
    """
    Tests running this within the fixtures dir.
    """

    with cd(FIXTURES_DIR):
        test_dir = Path("successfull_test_suite")
        assert test_dir.is_dir()
        run_tests(test_dir)

    stdout, stderr = capfd.readouterr()

    assert (
        re.search(r"defined \w+: \d+ bytes?", stdout) is None
    ), "Should not find Foma output in successfull test run"

    assert "No FST test cases found" not in stdout, "Emtpy test suite?"
    assert "Failed" not in stdout, "Failed test suite?"
    assert re.search(r"(\d+)/\1 passed!", stdout)


# Copied from: https://stackoverflow.com/a/24469659/6626414
@contextlib.contextmanager
def cd(path):
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)
