# ArthAI — Adaptive Security Layer

Reusable, financial-grade threat definitions, detection rules, mitigations and
incident history for ArthAI, driven by [`SECURITY_POLICY.md`](SECURITY_POLICY.md)
and validated automatically in CI.

The layer lives in [`security/`](security/README.md): 12 threat definitions
(`ASDR-*`), detection rules (`RULE-SEC-*`), mitigation runbooks (`MITIG-*`),
sanitized incident records (`INC-*`) and JSON schemas.

## Validation

The layer is validated deterministically — required structure, YAML/JSON
parsing, schema conformance, cross-references and a secret-literal scope guard:

```bash
python3 security/tests/validate_security.py
```

Requires only PyYAML. A convenience wrapper and a pytest suite are included:

```bash
python3 cli.py
pytest -q
```

## Layout

See [`security/README.md`](security/README.md) for the full directory map and
[`SECURITY_POLICY.md`](SECURITY_POLICY.md) for the governing policy.

## MCP Server

This repository ships a dependency-free [Model Context Protocol](https://modelcontextprotocol.io)
stdio server so assistants, agents and [glama.ai](https://glama.ai) can inspect the project.

```bash
python3 mcp_server.py
```

Tools: `repo_info`, `list_files`, `read_file`, `search`, `health`. Standard library only — no
installation or dependencies required. Listing metadata is declared in [`glama.json`](glama.json).
