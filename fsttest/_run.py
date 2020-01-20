#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
from pathlib import Path
from typing import Any, Dict, Optional

import toml
from blessings import Terminal  # type: ignore

from ._fst import FST
from ._results import TestResults
from ._test_case import TestCase

# ############################### Constants ################################ #

# Exit codes
_EX_BASE = 0x40
EX_NO_TEST_CASES = _EX_BASE + 1
EX_HAS_FAILED_TEST_CASES = _EX_BASE + 2


# ################################ Globals ################################# #

term = Terminal()


# ############################### Functions ################################ #


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
            if results.has_test_failures:
                diag = fst.diagnostics
                if diag is not None:
                    print(fst.diagnostics, file=sys.stderr)
                else:
                    print(
                        f"{term.yellow}{term.italic}No diagnostics available",
                        f"for fst defined in {test_file}{term.normal}",
                        file=sys.stderr,
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
