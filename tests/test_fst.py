#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test using the FST class.
"""

from pathlib import Path

import pytest  # type: ignore

from fsttest import FST


def test_path_exists_only_during_command_fomabin(a_b_transducer_path: Path):
    """
    Test that a new Fomabin is created and disappears after the context.
    """
    fst_desc = {"fomabin": a_b_transducer_path}
    with FST.load_from_description(fst_desc) as fst:
        assert fst.path.exists()
    assert not fst.path.exists()


def test_load_from_path(a_b_transducer_path: Path):
    """
    Test that an FST can be used from an existing path.
    """
    with FST.load_from_path(a_b_transducer_path) as fst:
        assert fst.path.exists()
        assert fst.path != a_b_transducer_path

        assert fst.apply(["a"], direction="down") == {"a": ["b"]}

    assert not fst.path.exists()


@pytest.mark.parametrize(
    "fst_desc",
    [{"regex": "Cleanup"}, {"compose": ["TInsertion", "NiTDeletion", "Cleanup"]},],
)
def test_path_exists_only_during_command_xfst(fst_desc, rewrite_rules_path: Path):
    """
    Test that the FST can be loaded from an XFST script.
    """
    fst_desc["eval"] = rewrite_rules_path
    with FST.load_from_description(fst_desc) as fst:
        assert fst.path.exists()
    assert not fst.path.exists()


def test_fst_execute_fomabin(a_b_transducer_path: Path):
    fst_desc = {"fomabin": a_b_transducer_path}
    with FST.load_from_description(fst_desc) as fst:
        results = fst.apply(["a"], direction="down")
    assert results == {"a": ["b"]}
