#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Union

import toml
from blessings import Terminal  # type: ignore

from ._fst import FST
from ._results import FailedTestResult, PassedTestResult, TestResults
from .exceptions import TestCaseDefinitionError

# ############################### Constants ################################ #

# Exit codes
_EX_BASE = 0x40
EX_NO_TEST_CASES = _EX_BASE + 1
EX_HAS_FAILED_TEST_CASES = _EX_BASE + 2


# ################################ Globals ################################# #

term = Terminal()


# ################################ Classes ################################# #


class TestCase:
    """
    An executable test case.
    """

    def __init__(
        self, input_: str, expected: str, direction: str, location: Optional[Path]
    ):
        self.input = input_
        self.expected = expected
        self.direction = direction
        self.location = location

    def execute(self, fst: FST) -> Union["PassedTestResult", "FailedTestResult"]:
        transductions = fst.apply([self.input], direction=self.direction)
        assert (
            self.input in transductions
        ), f"Expected to find {self.input} in {transductions}"

        actual_transductions = transductions[self.input]

        if self.expected in actual_transductions:
            return PassedTestResult(location=self.location)
        else:
            return FailedTestResult(
                given=self.input,
                expected=self.expected,
                actual=actual_transductions,
                location=self.location,
            )

    @staticmethod
    def from_description(
        raw_test_case: Dict[str, Any], location: Optional[Path] = None
    ) -> "TestCase":
        """
        Given a dictionary, parses and returns an executable test case.
        """
        # Parse a few things
        if "expect" not in raw_test_case:
            raise TestCaseDefinitionError('Missing "expect" in test case')
        expected = raw_test_case["expect"]

        if "upper" in raw_test_case:
            direction = "down"
            fst_input = raw_test_case["upper"]
        elif "lower" in raw_test_case:
            direction = "up"
            fst_input = raw_test_case["lower"]
        else:
            raise TestCaseDefinitionError('Missing "upper" or "lower" in test case')

        return TestCase(fst_input, expected, direction, location)


# ############################### Functions ################################ #


@contextmanager
def load_fst(fst_desc: Dict[str, Any]) -> Generator[Path, None, None]:
    return FST._load_fst(fst_desc)


def run_test_suite_from_filename(test_file: Path) -> TestResults:
    """
    Given a file path, parses the test suite, and runs all of the tests
    contained therein.
    """
    # Output looks like this:
    raw_test_case = toml.load(test_file)

    results = TestResults()

    fst_desc = raw_test_case["fst"]
    with FST.load_from_description(fst_desc) as fst:
        # Raw test cases look like this:
        # {
        #     "tests": [
        #         {"upper": "ki<ajan", "expect": "kitajan"},
        #         {"upper": "ni<ajan", "expect": "nitajan"},
        #     ],
        # }
        for test_case in raw_test_case["tests"]:
            results_from_test_case = execute_test_case(
                fst.path, test_case, location=test_file
            )
            results.update_in_place(results_from_test_case)

    return results


def run_tests(test_dir: Path) -> None:
    """
    Run all tests in the given test directory path.

    Files that are tested match the glob pattern:

        test_*.toml

    e.g.,

     * test_vai_inflection.toml
     * test_t_epenthesis.toml
     * test_analyze_noun.toml

    are all tests that will be matched.
    """

    results = TestResults()

    tests = test_dir.glob("test_*.toml")
    for test_file in tests:
        results_from_test_suite = run_test_suite_from_filename(test_file)
        results.update_in_place(results_from_test_suite)

    if results.has_test_failures:
        for failure in results.test_failures:
            print(f"{term.red}{failure}{term.normal}", file=sys.stderr)
        print(f"💥 {term.red}Failed {results.n_failed} test cases{term.normal} 😭😭😭")
        print(f"{term.bold}({results.n_passed}/{results.n_total}) passed{term.normal}")
        sys.exit(EX_HAS_FAILED_TEST_CASES)
    elif results.n_total == 0:
        print(f"{term.red}No FST test cases found.{term.normal} 🤔")
        sys.exit(EX_NO_TEST_CASES)
    else:
        print(
            f"{term.bold}{results.n_passed}/{results.n_total} tests passed!{term.normal} ✨ 🍰 ✨"
        )


def execute_test_case(
    fst_path: Path, raw_test_case: Dict[str, Any], location: Optional[Path] = None
) -> TestResults:
    """
    Execute a test case from its raw dictionary.
    """

    test_case = TestCase.from_description(raw_test_case, location=location)

    with FST.load_from_path(fst_path) as fst:
        result = test_case.execute(fst)

    results = TestResults()
    results.append(result)

    return results
