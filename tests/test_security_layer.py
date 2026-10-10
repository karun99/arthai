"""Runs the ArthAI security-layer validation suite under pytest."""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(ROOT, "security", "tests", "validate_security.py")


def test_security_layer_is_valid():
    result = subprocess.run([sys.executable, VALIDATOR], cwd=ROOT)
    assert result.returncode == 0, "security-layer validation failed"
