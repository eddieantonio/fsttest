#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from fsttest import TestResults as _TestResults


def test_existence_of_test_results() -> None:
    results = _TestResults()
    assert results.n_total == 0
