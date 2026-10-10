#!/usr/bin/env python3
"""ArthAI Adaptive Security Layer — command-line entry point.

Runs the deterministic validation suite that keeps the security layer
coherent. Equivalent to ``python3 security/tests/validate_security.py``.
"""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(ROOT, "security", "tests", "validate_security.py")


def main(argv: list | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    return subprocess.call([sys.executable, VALIDATOR, *argv])


if __name__ == "__main__":
    raise SystemExit(main())
