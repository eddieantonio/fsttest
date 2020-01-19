#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path

import pytest  # type: ignore

from fsttest import FST, FailedTestResult, PassedTestResult
from fsttest import TestCase as _TestCase


@pytest.mark.parametrize(
    "raw_test_case,fst_input,expected,direction",
    [
        ({"upper": "a", "expect": "b"}, "a", "b", "down"),
        ({"lower": "b", "expect": "a"}, "b", "a", "up"),
    ],
)
@pytest.mark.parametrize(
    "location", [None, "test_verbs.toml"],
)
def test_create_test_case(
    raw_test_case, fst_input: str, expected: str, direction: str, location
):
    t = _TestCase.from_description(raw_test_case, location=location)
    assert t.input == fst_input
    assert t.expected == expected
    assert t.direction == direction
    assert t.location == location


@pytest.mark.parametrize(
    "raw_test_case,location",
    [
        ({"upper": "a", "expect": "b"}, "test_verbs.toml"),
        ({"lower": "b", "expect": "a"}, None),
    ],
)
def test_create_passed_test_from_test_case(raw_test_case, location):
    t = _TestCase.from_description(raw_test_case, location=location)
    res = PassedTestResult.from_test_case(t)
    assert t.location == res.location


def test_execute_passing_test_case(a_b_transducer_path: Path):
    test_case = _TestCase.from_description(
        {"upper": "a", "expect": "b"}, location="test_verbs.toml"
    )
    with FST.load_from_path(a_b_transducer_path) as fst:
        result = test_case.execute(fst)
    assert isinstance(result, PassedTestResult)


def test_execute_failing_test_case(a_b_transducer_path: Path):
    test_case = _TestCase.from_description(
        {"upper": "a", "expect": "a"}, location="test_verbs.toml"
    )
    with FST.load_from_path(a_b_transducer_path) as fst:
        result = test_case.execute(fst)
    assert isinstance(result, FailedTestResult)
    assert result.location == test_case.location
    assert result.input == "a"
    assert result.expected == "a"
    assert result.actual == ["b"]
