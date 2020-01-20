#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Represent test results.
"""

from pathlib import Path
from typing import Any, Iterable, List, Optional, Set, Union


class PassedTestResult:
    """
    Represents one passed test.
    """

    def __init__(self, location: Optional[Path]):
        self._location = location

    @property
    def location(self) -> Optional[Path]:
        return self._location


class FailedTestResult:
    """
    Represents a failed test. Contains the reason WHY the test failed.
    """

    def __init__(
        self, given: str, expected: str, actual: Any, location: Optional[Path] = None
    ):
        self._location = location
        self._input = given
        self._expected = expected
        self._actual = actual

    @property
    def location(self) -> Optional[Path]:
        return self._location

    @property
    def input(self) -> str:
        return self._input

    @property
    def expected(self) -> str:
        return self._expected

    @property
    def actual(self) -> str:
        return self._actual

    def __str__(self) -> str:
        location = self.location or "<unknown>"
        return (
            f"{location}: Failure:\n"
            f"  Given: {self.input!r}\n"
            f"  Expected: {self.expected!r}\n"
            f"  Instead, got: {self.actual!r}"
        )


class TestResults:
    """
    Keeps track of test results.
    """

    def __init__(self, passed: int = 0, failed: int = 0) -> None:
        self.n_passed = passed
        self._n_failed = failed
        self._test_failures: List[FailedTestResult] = []

    @property
    def n_total(self) -> int:
        return self.n_passed + self.n_failed

    @property
    def n_failed(self) -> int:
        return self._n_failed + len(self._test_failures)

    @property
    def has_test_failures(self) -> bool:
        """
        True if there are any test failures; false, otherwise.
        """
        return self.n_failed > 0

    @property
    def test_failures(self) -> Iterable[FailedTestResult]:
        """
        Yields all failed test results.
        """
        return iter(self._test_failures)

    @property
    def location_of_test_failures(self) -> Set[Optional[Path]]:
        return {res.location for res in self._test_failures}

    def append(self, result: Union[PassedTestResult, FailedTestResult]) -> None:
        """
        Append a test result and count it.
        """
        if isinstance(result, PassedTestResult):
            self.n_passed += 1
        elif isinstance(result, FailedTestResult):
            self._test_failures.append(result)

    def update_in_place(self, other: "TestResults") -> "TestResults":
        """
        Updates these results with another results object.
        """

        previous_total = self.n_total

        self.n_passed += other.n_passed
        self._n_failed += other._n_failed
        self._test_failures.extend(other._test_failures)

        assert self.n_total == previous_total + other.n_total
        return self
