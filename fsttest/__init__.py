#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
FST test -- test your Foma finite-state transducers!
"""

from .__version__ import VERSION as __version__
from ._fst import FST
from ._results import FailedTestResult, PassedTestResult, TestResults
from ._run import execute_test_case, run_tests
from ._test_case import TestCase
from .exceptions import FSTTestError, TestCaseDefinitionError

__all__ = [
    "FST",
    "FSTTestError",
    "FailedTestResult",
    "PassedTestResult",
    "TestCase",
    "TestCaseDefinitionError",
    "TestResults",
    "execute_test_case",
    "run_tests",
]
