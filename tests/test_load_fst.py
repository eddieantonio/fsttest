#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test everything from FST tests, for now.
"""

from pathlib import Path

import pytest  # type: ignore

# Pytest will try to run tests here.
from fsttest import FST
from fsttest import TestCaseDefinitionError as _TestCaseDefinitionError
from fsttest import execute_test_case


def test_load_fst_from_fomabin(a_b_transducer_path: Path):
    """
    Test that the FST can be loaded from a fomabin.
    """

    # Check that we can load this FST directly.
    fst_desc = {"fomabin": a_b_transducer_path}
    test_case = {"upper": "a", "expect": "b"}

    with FST.load_from_description(fst_desc) as fst:
        results = execute_test_case(fst.path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


def test_load_fst_from_xfst_file(rewrite_rules_path: Path):
    """
    Test that the FST can be loaded from an XFST script.
    """
    fst_desc = {"eval": rewrite_rules_path, "regex": "Cleanup"}
    test_case = {"upper": "<", "expect": ""}
    with FST.load_from_description(fst_desc) as fst:
        results = execute_test_case(fst.path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


@pytest.mark.parametrize(
    "test_case",
    [
        {"upper": "ni<ayaa<n", "expect": "dayaan"},
        {"upper": "ki<ayaa<n", "expect": "kitayaan"},
    ],
)
def test_load_fst_from_xfst_with_compose(test_case, rewrite_rules_path: Path):
    """
    Using the 'compose' feature to load an XFST script with multiple defined
    regexes.
    """
    rules = ["TInsertion", "NiTDeletion", "Cleanup"]
    fst_desc = {"eval": rewrite_rules_path, "compose": rules}
    with FST.load_from_description(fst_desc) as fst:
        results = execute_test_case(fst.path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1
