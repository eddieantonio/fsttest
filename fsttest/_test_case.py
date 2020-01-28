#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ._fst import FST
from ._results import FailedTestResult, PassedTestResult
from .exceptions import TestCaseDefinitionError


class TestCase:
    """
    An executable test case.
    """

    def __init__(
        self, input_: str, expected: List[str], direction: str, location: Optional[Path]
    ):
        self.input = input_
        self.expected = expected
        self.direction = direction
        self.location = location

    def execute(self, fst: FST) -> Union[PassedTestResult, FailedTestResult]:
        transductions = fst.apply([self.input], direction=self.direction)
        assert (
            self.input in transductions
        ), f"Expected to find {self.input} in {transductions}"

        actual_transductions = transductions[self.input]

        assert len(self.expected) >= 1, "Must have at least on expected output"
        if set(self.expected) <= set(actual_transductions):
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
        raw_expected = raw_test_case["expect"]
        if isinstance(raw_expected, str):
            expected = [raw_expected]
        elif isinstance(raw_expected, list):
            if len(raw_expected) == 0:
                raise TestCaseDefinitionError(
                    "Must provide at least one expected transduction"
                )
            expected = raw_expected
        else:
            raise TestCaseDefinitionError(
                '"expect" MUST be either a single string or a list of strings;'
                f"instead got {raw_expected!r}"
            )

        if "upper" in raw_test_case:
            direction = "down"
            fst_input = raw_test_case["upper"]
        elif "lower" in raw_test_case:
            direction = "up"
            fst_input = raw_test_case["lower"]
        else:
            raise TestCaseDefinitionError('Missing "upper" or "lower" in test case')

        return TestCase(fst_input, expected, direction, location)
