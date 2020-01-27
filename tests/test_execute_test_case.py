#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test executing test cases from plain Python objects.
"""

from pathlib import Path

import pytest  # type: ignore

# Pytest will try to run tests here.
from fsttest import TestCaseDefinitionError as _TestCaseDefinitionError
from fsttest import execute_test_case


def test_transduce_upper_to_lower(a_b_transducer_path: Path):
    """
    Test a successful upper -> lower test case.
    """
    test_case = {"upper": "a", "expect": "b"}
    results = execute_test_case(a_b_transducer_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


def test_transduce_lower_to_upper(a_b_transducer_path: Path):
    """
    Test a successful lower -> upper test case.
    """
    test_case = {"lower": "b", "expect": "a"}
    results = execute_test_case(a_b_transducer_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


def test_failed_test_case(a_b_transducer_path: Path):
    """
    Test when a test case fails.
    """
    test_case = {"upper": "a", "expect": "a"}
    results = execute_test_case(a_b_transducer_path, test_case)

    assert results.n_passed == 0
    assert results.n_failed == 1
    assert results.n_total == 1


def test_invalid_test_case(a_b_transducer_path: Path):
    """
    Test that an under-specified test case raises an error.
    """

    test_case = {"upper": "a"}
    with pytest.raises(_TestCaseDefinitionError):
        execute_test_case(a_b_transducer_path, test_case)


def test_transduce_multiple_expects(cactus_transducer_path: Path):
    """
    Test a successful upper -> lower test case.
    """
    test_case = {"upper": "cactus[PL]", "expect": ["cactuses", "cacti"]}
    results = execute_test_case(cactus_transducer_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1
