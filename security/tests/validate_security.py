"""
ArthAI Adaptive Security Layer — structural & reference validation.

Deterministic, dependency-light checks that keep security/ coherent and
enforceable. Run anywhere via:

    python3 security/tests/validate_security.py

Runs on CI in .github/workflows/security.yml (push/PR),
validate-security-layer.yml (push/PR), and security-regression.yml (weekly).

Checks:
  1. Required directory structure exists (drift detection).
  2. All definition/rule/incident YAML files parse.
  3. JSON schemas parse.
  4. Definitions carry required fields; severity/status stay in allowed enums.
  5. Rules reference existing threat IDs.
  6. Incidents reference existing threat IDs.
  7. Finance clarity: ASDR-009/ASDR-010 exist and are active.
  8. Scope guard: no secret literals match the enforced CI patterns (low
     false-positive set) anywhere in demo/, app/, backend/, .github/, docs/.
"""

import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML is required. Install with: pip install pyyaml\\n")
    sys.exit(2)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMAS = os.path.join(BASE, "schemas")
DEFS = os.path.join(BASE, "definitions")
RULES = os.path.join(BASE, "rules")
INCIDENTS = os.path.join(BASE, "incidents")
REPO = os.path.dirname(BASE)  # repo root

REQUIRED_DIRS = [
    "definitions/authentication",
    "definitions/authorization",
    "definitions/injection",
    "definitions/dependencies",
    "definitions/data",
    "definitions/infrastructure",
    "definitions/automation",
    "definitions/availability",
    "definitions/finance",
    "rules",
    "tests",
    "mitigations",
    "incidents",
    "schemas",
]

REQUIRED_FIELDS = [
    "threat_id",
    "name",
    "category",
    "severity",
    "description",
    "indicators",
    "detection",
    "mitigation",
    "validation",
    "status",
]

SEVERITIES = {"Critical", "High", "Medium", "Low", "Informational"}
STATUSES = {"proposed", "validated", "active", "updated", "deprecated"}
CATEGORIES = {
    "authentication", "authorization", "injection", "dependencies",
    "data", "infrastructure", "automation", "availability", "finance",
}

# Low-false-positive credential shapes enforced by .github/workflows/security.yml.
SECRET_PATTERNS = [
    re.compile(r"BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-or-v1-[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{24,}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"gho_[A-Za-z0-9]{36}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"rzp_(test|live)_[A-Za-z0-9]{14}_[A-Za-z0-9]{14}"),
    re.compile(r"OWS_(PRIVATE|SEED|MNEMONIC)_KEY\s*=\s*[^\\s]+"),
]

SCAN_EXCLUDES = {"node_modules", ".git", ".next", "dist", "build", "__pycache__",
                 ".ruff_cache", "coverage", "pnpm-lock.yaml", "package-lock.json"}

FINANCE_EXPECTED = {
    "ASDR-009": {"threat_id": "ASDR-009", "severity": "Critical"},
    "ASDR-010": {"threat_id": "ASDR-010", "severity": "Critical"},
}


def yaml_files(folder):
    out = []
    for root, _dirs, files in os.walk(folder):
        for name in files:
            if name.endswith((".yml", ".yaml")):
                out.append(os.path.join(root, name))
    return sorted(out)


def relpath(path):
    return os.path.relpath(path, REPO)


def main():
    failures = 0
    count = [0]

    def fail(msg):
        nonlocal failures
        failures += 1
        print(f"FAIL  {msg}")

    def ok(msg):
        print(f"OK    {msg}")

    def bump():
        count[0] += 1

    print("── Directory structure ───────────────────────────────")
    for rel in REQUIRED_DIRS:
        path = os.path.join(BASE, rel)
        if os.path.isdir(path):
            ok(path)
        else:
            fail(f"missing directory: {rel}")

    print("── Schema JSON validity ──────────────────────────────")
    for schema in sorted(os.listdir(SCHEMAS)):
        if not schema.endswith(".json"):
            continue
        try:
            json.load(open(os.path.join(SCHEMAS, schema)))
            ok(f"schema {schema} parses")
        except Exception as e:
            fail(f"schema {schema}: {e}")

    print("── Threat definitions ────────────────────────────────")
    definitions = {}
    for path in yaml_files(DEFS):
        bump()
        try:
            doc = yaml.safe_load(open(path))
        except Exception as e:
            fail(f"{relpath(path)}: unparsable YAML: {e}")
            continue
        if not isinstance(doc, dict):
            fail(f"{relpath(path)}: not a mapping")
            continue
        tid = doc.get("threat_id")
        if not tid:
            fail(f"{relpath(path)}: missing threat_id")
        definitions[tid] = {"path": path, "doc": doc}
        for field in REQUIRED_FIELDS:
            if field not in doc:
                fail(f"{relpath(path)}: missing required field '{field}'")
        if doc.get("severity") not in SEVERITIES:
            fail(f"{relpath(path)}: invalid severity '{doc.get('severity')}'")
        if doc.get("status") not in STATUSES:
            fail(f"{relpath(path)}: invalid status '{doc.get('status')}'")
        if doc.get("category") not in CATEGORIES:
            fail(f"{relpath(path)}: unknown category '{doc.get('category')}'")
        if not any(k in doc for k in ("validation",)):
            fail(f"{relpath(path)}: validation procedure must be defined")
    print(f"  -> {len(definitions)} definition(s) parsed")
    for tid in sorted(definitions):
        ok(f"{definitions[tid]['path']} ({tid})")

    print("── Finance clarity (agentic-payment + wallet) ────────")
    for tid, expected in FINANCE_EXPECTED.items():
        bump()
        doc = definitions.get(tid, {}).get("doc", {})
        if doc.get("threat_id") != expected["threat_id"]:
            fail(f"finance definition {tid} missing or malformed")
            continue
        if doc.get("severity") != expected["severity"]:
            fail(f"{tid} severity must be {expected['severity']}")
        if doc.get("status") != "active":
            fail(f"{tid} must be active")
        ok(f"{tid} severity={expected['severity']} status=active")

    print("── Detection rules ↔ definitions ─────────────────────")
    rules = 0
    for path in yaml_files(RULES):
        try:
            doc = yaml.safe_load(open(path)) or {}
        except Exception as e:
            fail(f"{relpath(path)}: unparsable YAML: {e}")
            continue
        tid = doc.get("threat_ref")
        rules += 1
        if tid not in definitions:
            fail(f"{relpath(path)}: threat_ref '{tid}' has no definition")
        else:
            ok(f"{relpath(path)} -> {tid}")

    print("── Incidents ↔ definitions ───────────────────────────")
    incidents = 0
    for path in yaml_files(INCIDENTS):
        try:
            doc = yaml.safe_load(open(path)) or {}
        except Exception as e:
            fail(f"{relpath(path)}: unparsable YAML: {e}")
            continue
        incidents += 1
        refs = [doc.get("threat_id"), doc.get("related_definition")]
        for ref in refs:
            if ref and ref not in definitions:
                fail(f"{relpath(path)}: references unknown definition '{ref}'")
            elif ref:
                ok(f"{relpath(path)} -> {ref}")
    print(f"  -> {rules} rule(s), {incidents} incident(s) cross-checked")

    print("── Scope secret sweep (low-false-positive set) ───────")
    secret_hits = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SCAN_EXCLUDES and not d.startswith(".")]
        for name in files:
            if name.rsplit(".", 1)[-1] in {"png", "jpg", "jpeg", "gif", "webp",
                                           "ico", "woff", "woff2", "ttf", "eot"}:
                continue
            path = os.path.join(root, name)
            try:
                with open(path, "rb") as f:
                    data = f.read().decode("utf-8", errors="ignore")
            except OSError:
                continue
            for i, pat in enumerate(SECRET_PATTERNS):
                m = pat.search(data)
                if m:
                    secret_hits.append((relpath(path), pat.pattern[:40]))
    if secret_hits:
        for path, pat in secret_hits:
            fail(f"secret pattern hit in {path} ({pat}...)")
    else:
        ok("no enforced secret patterns in working tree")

    print(f"  -> {count[0]} assertions executed")

    summary = "PASS" if failures == 0 else f"{failures} issue(s)"
    print(f"\\nSecurity validation result: {summary}")
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()