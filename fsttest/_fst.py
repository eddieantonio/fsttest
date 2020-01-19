#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Define the FST class.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .exceptions import FSTTestError


class FST:
    def __init__(self, path: Path):
        self.path = path

    # @staticmethod
    # def load_from_description(fst_desc: Dict[str, Any]) -> FST:
    #     return FST(...)


def determine_foma_args(raw_fst_description: dict) -> List[str]:
    """
    Given an FST description, this parses it and returns arguments to be
    passed to foma(1) in order to leave the desired tranducer on the top of
    the foma stack.
    """

    # What the TOML looks like:
    #     "fst": {"eval": "phon_rules.xfscript", "regex": "TInsertion"},

    args: List[str] = []

    # First, load whatever needs to be loaded.
    if "eval" in raw_fst_description:
        # Load an XFST script
        file_to_eval = Path(raw_fst_description["eval"])
        assert file_to_eval.exists()
        args += ["-l", str(file_to_eval)]
    elif "fomabin" in raw_fst_description:
        # Load a fomabin
        path = Path(raw_fst_description["fomabin"])
        assert path.exists()
        args += ["-e", f"load stack {path}"]
    else:
        raise FSTTestError(f"Don't know how to read FST from: {raw_fst_description}")

    # TODO: implement other forms of loading the fst

    if "regex" in raw_fst_description:
        regex = raw_fst_description["regex"]
        assert isinstance(regex, str)
        args += ["-e", f"regex {regex};"]
    elif "compose" in raw_fst_description:
        compose = raw_fst_description["compose"]
        assert isinstance(compose, list)
        # .o. is the compose regex operation
        regex = " .o. ".join(compose)
        args += ["-e", f"regex {regex};"]
    # else, it uses whatever is on the top of the stack.

    return args
