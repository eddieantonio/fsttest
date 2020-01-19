#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from fsttest import TestCase as _TestCase


def test_create_test_case():
    t = _TestCase.from_description({"upper": "a", "expect": "b"})
    assert t.input == "a"
    assert t.expected == "b"
