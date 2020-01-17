#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test everything from FST tests, for now.
"""

from pathlib import Path

import pytest  # type: ignore

# Pytest will try to run tests here.
from fsttest import TestCaseDefinitionError as _TestCaseDefinitionError
from fsttest import execute_test_case, load_fst


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


def test_failed_test_case(a_b_transducer_path: Path, capsys):
    """
    Test when a test case fails.
    """
    test_case = {"upper": "a", "expect": "a"}
    results = execute_test_case(a_b_transducer_path, test_case)

    assert results.n_passed == 0
    assert results.n_failed == 1
    assert results.n_total == 1

    captured = capsys.readouterr()
    assert "Failure" in captured.err
    assert "Given: 'a'" in captured.err
    assert "Expected: 'a'" in captured.err
    assert "got: ['b']" in captured.err


def test_invalid_test_case(a_b_transducer_path: Path):
    """
    Test that an under-specified test case raises an error.
    """

    test_case = {"upper": "a"}
    with pytest.raises(_TestCaseDefinitionError):
        execute_test_case(a_b_transducer_path, test_case)


def test_load_fst_from_fomabin(a_b_transducer_path: Path):
    """
    Test that the FST can be loaded from a fomabin.
    """

    # Check that we can load this FST directly.
    fst_desc = {"fomabin": a_b_transducer_path}
    test_case = {"upper": "a", "expect": "b"}

    with load_fst(fst_desc) as fst_path:
        results = execute_test_case(fst_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


def test_load_fst_from_xfst_file(rewrite_rules_path: Path):
    """
    Test that the FST can be loaded from an XFST script.
    """
    fst_desc = {"eval": rewrite_rules_path, "regex": "Cleanup"}
    test_case = {"upper": "<", "expect": ""}
    with load_fst(fst_desc) as fst_path:
        results = execute_test_case(fst_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


def test_load_fst_from_xfst_with_compose(rewrite_rules_path: Path):
    """
    Using the 'compose' feature to load an XFST script with multiple defined
    regexes.
    """
    rules = ["TInsertion", "NiTDeletion", "Cleanup"]
    fst_desc = {"eval": rewrite_rules_path, "compose": rules}
    test_case = {"upper": "ni<ayaa<n", "expect": "dayaan"}
    with load_fst(fst_desc) as fst_path:
        results = execute_test_case(fst_path, test_case)
    assert results.n_passed == 1
    assert results.n_total == 1


@pytest.fixture
def a_b_transducer_path() -> Path:
    """
    Transduces a (upper) to b (lower).
    """
    path = Path(__file__).parent / "fixtures" / "ab.fomabin"
    assert path.exists()
    return path


@pytest.fixture
def rewrite_rules_path() -> Path:
    """
    Returns the path to an XFST script with the following defined regexes:

     - Vowel
     - TInsertion
     - NiTDeletion
     - Cleanup
    """
    path = Path(__file__).parent / "fixtures" / "rewrite_rules.xfscript"
    assert path.exists()
    return path
