#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test using the FST class.
"""

from pathlib import Path

from fsttest import FST


def test_path_exists_during_command(a_b_transducer_path: Path):
    fst_desc = {"fomabin": a_b_transducer_path}
    with FST.load_from_description(fst_desc) as fst:
        assert fst.path.exists()
