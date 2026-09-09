# SECURITY_CHANGELOG — ArthAI

Records all security-policy and security-tooling changes in the arthai repository.

## 2026-09-09 — v1.0: Financial-grade security baseline

**Added**
- `SECURITY_POLICY.md` — Adaptive Financial Security Definition and Continuous
  Validation Framework (v1.0), including the mandatory **6-layer financial gate**
  (bounded, gated, explainable, anomaly, reputation, audit).
- `security/definitions/` — 10 active threat definitions (ASDR-001 … ASDR-010),
  including finance-specific:
  - `ASDR-009` Agentic Payment Fraud (Critical).
  - `ASDR-010` Wallet Key / Seed Exposure (Critical).
- `security/rules/RULE-SEC-001 … RULE-SEC-005` — enforced detection rules,
  including `RULE-SEC-002` (Razorpay/OpenRouter/JWT/DB-URL secrets) and
  `RULE-SEC-005` (wallet key & seed material gate).
- `security/mitigations/MITIG-001 … MITIG-010` — runbooks, one per threat.
- `security/incidents/INC-2026-001-baseline.yml` — clean baseline record.
- `security/schemas/` — definition + incident JSON schemas.
- `security/tests/validate_security.py` — dependency-light validation suite.
- `.github/dependabot.yml` — daily/weekly dependency updates for npm, pip, and
  GitHub Actions across `demo/`, `app/`, and `backend/`.
- `.github/workflows/security.yml` — Gitleaks + hardcoded-secret block (incl.
  wallet patterns) + workflow/config validation.
- `.github/workflows/codeql.yml` — CodeQL static analysis (js/ts + python).
- `.github/workflows/dependency-review.yml` — PR gate on vulnerable dependencies.
- `.github/workflows/security-regression.yml` — weekly re-scan + rule self-test
  + validation suite (Monday 03:30 UTC, manual dispatch).
- `.github/workflows/validate-security-layer.yml` — push/PR pass validating the
  security layer itself (schemas, YAML coherence, rule/incident references).
- `.env.example` (placeholders only) and `.gitignore` (secret/credential
  exclusions).

**Definition status**
- ASDR-001 … ASDR-010 — `active`.
- RULE-SEC-001 … RULE-SEC-005 — enforced.

## Planned

- Phase 2: policy-engine unit/integration test matrix (6-layer gate).
- Phase 3: secrets baseline scan script (`security/tests/history_scan.sh`).
- Phase 4: incident memory automation for the weekly regression scan.