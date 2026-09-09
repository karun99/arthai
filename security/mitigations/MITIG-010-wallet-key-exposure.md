# MITIG-010 — Wallet Key / Seed Exposure

**Threat:** ASDR-010 — Wallet Key / Seed Exposure

## Steps

1. **Contain** — **loss-of-funds**: immediately move funds out of the exposed wallet to a fresh address, disable the OWS/Circle key, and revoke the x402 signing material. This outranks all other work.
2. **Identify** — where material leaked: repo/history, client bundle (NEXT_PUBLIC_), agent runtime env, logs, vector-store metadata.
3. **Fix**
   - Wallet secrets exist only as env vars injected into the OWS MCP process at runtime.
   - Agent processes sign via the gateway and never hold keys (non-custodial).
   - Strip wallet material from logs/telemetry; scrub transitive artifacts (Redis, ChromaDB, Neo4j).
   - Mount wallet dirs read-only; run wallet service as non-root.
4. **Validate** — RULE-SEC-005 gate passes against full history; agent-integration test asserts the agent cannot read key files (file permissions); log assertion shows no signing material in audit samples.
5. **Regression** — RULE-SEC-005 + gitleaks stay enforced on push/PR and weekly regression re-scan.

## Definition update
Record sanitized INC; update `ASDR-010`.