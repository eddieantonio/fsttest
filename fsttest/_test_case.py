#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from typing import Any, Dict, Optional, Union

from ._fst import FST
from ._results import FailedTestResult, PassedTestResult
from .exceptions import TestCaseDefinitionError


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
