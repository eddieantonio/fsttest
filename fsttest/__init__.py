#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
FST test -- test your finite-state transducers!
"""

from .fsttest import (
    FSTTestError,
    TestCaseDefinitionError,
    TestResults,
    execute_test_case,
    run_tests,
)
from .__version__ import VERSION as __version__

__all__ = [
    "FSTTestError",
    "TestCaseDefinitionError",
    "run_tests",
    "TestResults",
    "execute_test_case",
]
