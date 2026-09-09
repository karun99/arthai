# MITIG-009 — Agentic Payment Fraud

**Threat:** ASDR-009 — Agentic Payment Fraud

## Steps

1. **Contain** — a fraudulent/phantom payment is **loss-of-funds**: one-click freeze of the affected merchant account, disable the agent's payment tool, revoke any suspect recipient list, and stop the x402 gateway/Razorpay payout scope. File dispute/recovery with Razorpay/Circle where applicable.
2. **Identify** — which gate failed: intent forgery (prompt injection), budget/cap bypass, missing/misordered approval, broken idempotency, skipped reputation or anomaly check.
3. **Fix**
   - Route **every** payment intent through the single choke point `app/lib/policy-engine.ts` (enforce 6-layer gate) — no direct Razorpay/Circle/MCP calls from agent code.
   - Approval above threshold requires recorded `{approved_by, approved_at}` before execution; no approvals retroactively.
   - Idempotency: `SHA-256(action_id+merchant_id+amount+nonce)`, Redis atomic lock, cached result on replay.
   - Reputation-check recipients on both fiat and crypto rails before transfer.
   - Anomaly detection (IsolationForest) runs pre-execution; block on flags.
   - VPersuas full-chain audit log at every stage incl. decisions and rejections.
4. **Validate** — unit tests: double-submit → one charge; over-cap → blocked; missing approval → blocked; unsigned x402 → refused. Re-run the whole suite.
5. **Regression** — keep the 6-layer test matrix permanent; static guard blocks payment SDK calls outside the gateway.

## Definition update
Record sanitized INC immediately (this is the highest-priority memory to write); update `ASDR-009`.