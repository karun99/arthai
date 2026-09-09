# MITIG-005 — Sensitive KYC / PII Data Exposure

**Threat:** ASDR-005 — Sensitive KYC / PII Data Exposure

## Steps

1. **Contain** — any leaked PII in bundles/logs: rotate the storage/session context and remove the artifact from CDN/history. Notify per governing law if exposure involved real users.
2. **Identify** the sink: console.error, error envelope, client bundle (NEXT_PUBLIC_), vector store, API DTO.
3. **Fix**
   - Encrypt KYC columns at rest (AES-256); keep raw PII out of both logs and client bundles.
   - Scrub log formatters/error handlers; never reflect request bodies in errors.
   - Vendor endpoints return only anonymized, aggregate SPI — no PII fields in response DTO.
   - ChromaDB/Neo4j documents keyed on pseudonymous IDs; no raw names/emails stored there.
   - Demo dataset synthetic only; add a fateful marker for "fake data" in mock-data.ts.
4. **Validate** — unit test: KYC payload through logger/error path emits zero PII; schema test: vendor endpoint response has no PII keys.
5. **Regression** — keep scrub tests; CodeQL taint check on PII sinks; PII review checklist on every form/route PR.

## Definition update
Record sanitized INC; update `ASDR-005` if a new sink type was exposed.