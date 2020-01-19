#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path

from fsttest import FailedTestResult
from fsttest import TestResults as _TestResults


def test_existence_of_test_results() -> None:
    results = _TestResults()
    assert results.n_total == 0


def test_can_count_a_passed_test_case() -> None:
    results = _TestResults()
    results.append(
        FailedTestResult(
            location=Path("test_verbs.toml"), given="a", expected="a", actual=["b"]
        )
    )
    assert results.n_failed == 1
    assert results.n_passed == 0
    assert results.n_total == 1
