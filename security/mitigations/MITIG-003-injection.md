# MITIG-003 — Injection

**Threat:** ASDR-003 — Injection

## Steps

1. **Contain** — if the vector is the S-AI spawn endpoint, disable it (or run it off the hot path) until patched.
2. **Identify** the injection sink: `child_process.spawn`/`exec`, string-built SQL/Cypher, unescaped prompt templates.
3. **Fix**
   - Replace any `exec`/`shell:true` with argument-array `spawn`; never pass user strings to a shell.
   - Parameterize all SQL and Cypher (no string interpolation for values).
   - Treat LLM output as untrusted: validate against an allow-schema; never feed output directly into a payment call.
   - Add prompt-delimiter hygiene around user text sent to the S-AI swarm.
4. **Validate** — fuzz the think/recommendation endpoints with malicious payloads; confirm tainted data cannot reach sinks; static check rejects `shell:true`.
5. **Regression** — keep fuzz fixtures; CodeQL injection queries run on push/PR.

## Definition update
Record incident; extend `ASDR-003` indicators if a new sink was discovered.