"""Run library tests that do not need a Quick EXE."""

from __future__ import annotations

import sys

import pytest

if __name__ == "__main__":
    raise SystemExit(pytest.main(["tests", "-m", "not live", "-q", *sys.argv[1:]]))
