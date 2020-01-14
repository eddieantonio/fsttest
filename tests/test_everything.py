#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test everything from FST tests, for now.
"""

from pathlib import Path

import pytest  # type: ignore

from fsttest import execute_test_case  # type: ignore


def test_transduce_upper_to_lower(a_b_transducer_path: Path):
    test_case = {"upper": "a", "expect": "b"}
    results = execute_test_case(a_b_transducer_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


def test_transduce_lower_to_upper(a_b_transducer_path: Path):
    test_case = {"lower": "b", "expect": "a"}
    results = execute_test_case(a_b_transducer_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


def test_failed_test_case(a_b_transducer_path: Path, capsys):
    test_case = {"upper": "a", "expect": "a"}
    results = execute_test_case(a_b_transducer_path, test_case)

    assert results.n_passed == 0
    assert results.n_failed == 1
    assert results.n_total == 1

    captured = capsys.readouterr()
    assert "Failure" in captured.err
    assert "Given: 'a'" in captured.err
    assert "Expected: 'a'" in captured.err
    assert "got: 'b'" in captured.err


@pytest.fixture
def a_b_transducer_path():
    """
    Transduces a (upper) to b (lower).
    """
    path = Path(__file__).parent / "fixtures" / "ab.fomabin"
    assert path.exists()
    return path
