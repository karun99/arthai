# MITIG-007 — Unsafe Automation

**Threat:** ASDR-007 — Unsafe Automation

## Steps

1. **Contain** — disable the risky workflow/agent token; revoke OIDC/permissions for the affected environment.
2. **Identify** the dangerous construct: `pull_request_target` running untrusted code, mutable action tags, over-scoped permissions, agent with push/deploy rights.
3. **Fix**
   - Pin actions to full commit SHAs (Dependabot keeps them updated).
   - Set `permissions: contents: read` minimum; only elevate what a job truly needs.
   - Never `pull_request_target` + checkout of PR head + script execution; gate untrusted inputs to run in a sandboxed, unprivileged job.
   - AI agents (S-AI style) get no direct push/payment tokens; all financial intent routes through `policy-engine.ts` with a human gate.
4. **Validate** — workflow lint rejects the dangerous patterns; PR simulation shows agents cannot reach financial MCP tools un-gated.
5. **Regression** — keep the workflow-integrity test (RULE-SEC-004) in CI on push/PR.

## Definition update
Record INC; update `ASDR-007` indicators if a new automation hazard appears.