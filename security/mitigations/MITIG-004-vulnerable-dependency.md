# MITIG-004 — Vulnerable Dependency / Supply Chain

**Threat:** ASDR-004 — Vulnerable Dependency / Supply Chain

## Steps

1. **Identify** the vulnerable package via Dependabot alert / advisory; confirm reachability (is it actually imported/executed?).
2. **Contain** — if the advisory is critical and reachable, prevent release: hold merges on the affected manifest.
3. **Fix** — apply the patched version (pin exact) via Dependabot security PR or manually; run the affected app's test suite.
4. **Fork audit** — for MCP server forks (`vyapaar-mcp`, `ows-mcp`, `razorpay-mcp`), `git diff` against upstream since last verified commit; re-verify before release.
5. **Validate** — `dependency-review.yml` passes; lockfile shows only the intended bump; builds reproduce in CI.
6. **Prevent** — purge unused deps; keep `package-lock`/`pnpm-lock`/`requirements.txt` committed; scope registry to official sources.

## Definition update
Record incident; update `ASDR-004` if this was a supply-chain shape not previously covered.