#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Define the FST class.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, Generator, List

from .exceptions import FSTTestError


class FST:
    def __init__(self, foma_args: List[str]):
        self._directory = tempdir = TemporaryDirectory()
        base = Path(tempdir.name)
        self._path = fst_path = base / "tmp.fomabin"
        status = subprocess.check_call(
            ["foma", *foma_args, "-e", f"save stack {fst_path!s}", "-s"]
        )

    def __enter__(self) -> FST:
        # Intiailization already done in __init__
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

        # Compile the FST first...
        foma_args = determine_foma_args(fst_desc)
        with FST(foma_args) as fst:
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
