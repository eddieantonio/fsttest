#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Define the FST class.
"""

from __future__ import annotations

import subprocess
from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, Generator, List

from .exceptions import FSTTestError


class FST:
    def __init__(self, foma_args: List[str]):
        self._directory = tempdir = TemporaryDirectory()
        base = Path(tempdir.name)
        self._path = fst_path = base / "tmp.fomabin"
        # Compile the FST:
        status = subprocess.check_call(
            ["foma", *foma_args, "-e", f"save stack {fst_path!s}", "-s"]
        )

    def __enter__(self) -> FST:
        # Note: Intiailization already done in __init__
        return self

    def __exit__(self, _exec_type, _exec, _stack):
        self._directory.cleanup()

    @property
    def path(self) -> Path:
        return self._path

    @staticmethod
    def load_from_description(fst_desc: Dict[str, Any]) -> FST:
        foma_args = determine_foma_args(fst_desc)
        return FST(foma_args)

    @staticmethod
    def _load_fst(fst_desc: Dict[str, Any]) -> Generator[Path, None, None]:
        """
        Loads an FST and yields its path. When finished using the FST, the path
        may no longer be used. Intended to be used in a with-statement:

            with load_fst({"eval": "./path/to/script.xfscript"}) as fst_path:
                ... # use fst_path
        """
        with FST.load_from_description(fst_desc) as fst:
            yield fst.path


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


def parse_lookup_output(raw_output: str) -> Dict[str, List[str]]:
    """
    Output from lookup, hfst-lookup and flookup is formatted as one
    transduction per line, with tab-separated values.

    Each line is formatted like this:

        {input}␉{transduction}

    If the FST is weighted, it will look like this:

        {input}␉{transduction}␉{weight}

    e.g.,

        eats    eat+Verb+3Person+Present
        eats    eat+Noun+Mass

    e.g., with weights:

        eats    eat+Verb+3Person+Present    0.54301
        eats    eat+Noun+Mass               7.63670

    If multiple strings are given as input, a blank line will (usually)
    separate transductions.

    If a transduction fails (cannot be analyzed), the transduction will be
    `+?` and the weight (if present) will be infinity.

    e.g.,

        fhqwhgads    +?      inf

    """

    results: Dict[str, List[str]] = defaultdict(list)

    for line in raw_output.splitlines():
        if not line.strip():
            # Ignore empty lines
            continue

        input_side, output_side, *_weight = line.lstrip().split("\t")
        results[input_side].append(output_side)

    return results
