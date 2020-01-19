#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pytest

from fsttest import TestCase as _TestCase


@pytest.mark.parametrize(
    "raw_test_case,fst_input,expected,direction",
    [({"upper": "a", "expect": "b"}, "a", "b", "down"),],
)
def test_create_test_case(raw_test_case, fst_input: str, expected: str, direction: str):
    t = _TestCase.from_description(raw_test_case)
    assert t.input == fst_input
    assert t.expected == expected
    assert t.direction == direction
