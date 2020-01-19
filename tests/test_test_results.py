#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path

from fsttest import FailedTestResult, PassedTestResult
from fsttest import TestResults as _TestResults


def test_existence_of_test_results() -> None:
    results = _TestResults()
    assert results.n_total == 0


def test_can_count_a_passed_test() -> None:
    results = _TestResults()
    results.append(PassedTestResult(location=Path("test_verbs.toml")))
    assert results.n_failed == 0
    assert results.n_passed == 1
    assert results.n_total == 1
    assert not results.has_test_failures
    assert len(results.location_of_test_failures) == 0


def test_can_count_a_test_failure() -> None:
    results = _TestResults()
    results.append(
        FailedTestResult(
            location=Path("test_verbs.toml"), given="a", expected="a", actual=["b"]
        )
    )
    assert results.n_failed == 1
    assert results.n_passed == 0
    assert results.n_total == 1
    assert results.has_test_failures
    assert results.location_of_test_failures == {Path("test_verbs.toml")}


def test_update_test_results_in_place() -> None:
    results = _TestResults()
    results.append(FailedTestResult(given="a", expected="a", actual=["b"]))
    assert results.n_total == 1
    assert results.n_failed == 1
    assert results.location_of_test_failures == {None}

    other_results = _TestResults()
    other_results.append(PassedTestResult(location=Path("test_awesome.toml")))
    other_results.append(
        FailedTestResult(
            given="b", expected="a", actual=["+?"], location=Path("test_verbs.toml")
        )
    )

    results.update_in_place(other_results)
    assert results.n_total == 3
    assert results.n_failed == 2
    assert results.location_of_test_failures == {None, Path("test_verbs.toml")}
