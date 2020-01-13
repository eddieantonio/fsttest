#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path

from fsttest import run_tests


def main():
    run_tests(Path("tests"))


assert __name__ == "__main__"
main()
