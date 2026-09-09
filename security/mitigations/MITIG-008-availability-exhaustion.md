# MITIG-008 — Availability Exhaustion

**Threat:** ASDR-008 — Availability Exhaustion

## Steps

1. **Contain** — rate-limit or temporarily disable the saturated endpoint; add a circuit breaker on the external provider.
2. **Identify** the exhaustion vector: unbounded loops, sync external calls in request handlers, missing rate limits, retry storms without idempotent backoff.
3. **Fix**
   - Add Redis rate limits (sliding window) on public endpoints.
   - Move LLM/webhook work to background queues; return 2xx fast after enqueueing.
   - Enforce idempotency-key backoff on all agent payment attempts.
   - Set timeouts and circuit breakers on LLM/Razorpay/Circle calls; set container resource limits + HEALTHCHECKs.
4. **Validate** — burst test (e.g., 1000 approval calls) is capped and budget not overspent; approval-screen timing assertion stays under 3s; webhook handler enqueues + returns promptly.
5. **Regression** — keep load+budget tests; revisit limits when traffic profile changes.

## Definition update
Record INC; update `ASDR-008` if a new exhaustion shape (e.g., webhook amplification) is found.