#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Define a few fixtures.
"""

from pathlib import Path

import pytest  # type: ignore


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
