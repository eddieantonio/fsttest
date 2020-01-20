#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import contextlib
import os
from pathlib import Path

import pytest  # type: ignore

from fsttest import run_tests

FIXTURES_DIR = Path(__file__).parent / "fixtures"
assert FIXTURES_DIR.is_dir()


def test_run(capsys) -> None:
    """
    Tests running this within the fixtures dir.
    """

    with pytest.raises(SystemExit):
        with cd(FIXTURES_DIR):
            test_dir = Path("test_suite_with_failures")
            assert test_dir.is_dir()
            run_tests(test_dir)

    stdout, stderr = capsys.readouterr()
    assert "No FST test cases found" not in stdout
    assert "Failed 1 test" in stdout
    assert "(1/2) passed" in stdout
    assert "test_a_b.toml: Failure" in stderr
    assert "Given: 'b'" in stderr
    assert "Expected: 'a'" in stderr


# Copied from: https://stackoverflow.com/a/24469659/6626414
@contextlib.contextmanager
def cd(path):
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)
