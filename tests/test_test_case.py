#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pytest  # type: ignore

from fsttest import PassedTestResult
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
