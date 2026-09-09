# SECURITY POLICY

## Adaptive Financial Security Definition and Continuous Validation Framework

**Repository:** `github.com/karun99/arthai`
**Policy Type:** Repository Security & Continuous Validation Policy (Financial-Grade)
**Version:** 1.0
**Status:** Active / Implementation Ready
**License:** CC BY 4.0 (this documentation component; see LICENSE)
**Last Updated:** 2026-09-09

---

## 1. Purpose

ArthAI is an agentic commerce gateway that moves **real money on both a fiat rail (Razorpay) and a crypto rail (x402 / Circle USDC)** on behalf of MSME vendors. Because AI-initiated financial transactions carry higher risk than human-initiated ones, this repository requires a continuous security framework beyond standard GitHub tooling.

This Security Policy establishes:

1. A structured, version-controlled definition repository of threats that apply specifically to an **AI-driven payments platform** (meanings: agentic execution, wallet custody, KYC data, hardware/cloud secrets).
2. Automated, always-on validation of the repository at commit, pull-request, dependency, and deployment stages.
3. A financial-governance overlay (the "6-layer safety gate": *bounded, gated, explainable, anomaly-detected, reputation-checked, audited*) that must hold before any AI-initiated action can execute.
4. A regression and incident memory so that a vulnerability remediated once is never silently reintroduced.

It complements GitHub-native mechanisms (Dependabot, CodeQL, Secret Scanning, dependency review) and the parent project's adaptive security layer (`proto-collection/SECURITY_POLICY.md`).

---

## 2. Security Objectives

This framework shall:

1. Identify threats specific to fiat + crypto payment orchestration, KYC data handling, wallet custody, and agentic execution.
2. Maintain machine- and human-readable definitions for every tracked threat (`ASDR-*`).
3. Detect unsafe changes automatically before they merge (`commit → PR → dependency → deploy`).
4. Enforce the 6-layer governance gate on every financial code path:
   - **Bounded** — every agent intent is constrained by a merchant budget/cap.
   - **Gated** — human/merchant approval is required above configured thresholds.
   - **Explainable** — every recommendation carries a complete, human-readable audit trace.
   - **Non-custodial by default** — wallet private keys never reach an agent process.
   - **Idempotent** — every payment carries a SHA-256 idempotency key.
   - **Auditable** — every action writes a full-chain log (VPersuas-style).
5. Keep secrets (Razorpay keys, OpenRouter keys, DB URLs, wallet mnemonics) out of the repository permanently.
6. Provide runbooks for incident response and remediation.
7. Track security regression so fixes stay fixed.
8. Maintain an auditable changelog of the security layer itself.

---

## 3. Scope

This policy applies to the entire `arthai` repository, including:

- `demo/` — cloud-deployed Next.js demo (mock data, no real transactions).
- `app/` — production Next.js application (live transactions).
- `backend/` — serverless/container services (`mcp-servers/`, `services/`, docker compose).
- `docs/`, `tests/`, configuration files, CI/CD workflows, deployment manifests, and generated artifacts.
- All integrations: Razorpay MCP, Vyapaar MCP, OWS MCP, x402/Circle, S-AI, ChromaDB, Neo4j, PostgreSQL, Redis, LLM providers.

Any code path that **moves money, stores PII/KYC, holds wallet material, or exposes an API surface** is in scope of the financial-grade controls in Sections 5–7.

---

## 4. Security Architecture

```
                   ┌──────────────────────────────────────┐
                   │          ArthAI Repository           │
                   └───────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │      GitHub Security Controls       │
                    │ Dependabot · CodeQL · Secret Scan   │
                    │ Dependency Review · Branch Rules    │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │   Adaptive Security Definition Layer │
                    │ (this repo: security/ + workflows)  │
                    └──────────────┬──────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
   Threat Definitions          Detection Rules          Mitigations
   (ASDR-001 … ASDR-010)      (RULE-SEC-*)            (MITIG-*)
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │      Continuous Validation (CI)      │
                    │ push · PR · dependency · weekly ·   │
                    │ deploy gate · scheduled regression  │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │      6-Layer Financial Gate         │
                    │ Bounded → Gated → Explainable →     │
                    │ Anomaly → Reputation → Audit        │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │     Incident Memory & Regression     │
                    └─────────────────────────────────────┘
```

The 6-layer financial gate is **code-level, not just CI-level**: it is implemented in `app/lib/policy-engine.ts` and, for the demo, mirrored in `demo/app/api/mock/governance/`. The security layer in this repo validates that those code paths stay present and correct.

---

## 5. Financial & Agentic Controls (Mandatory)

These controls are non-negotiable for any branch merged on `main` that touches payment, wallet, or KYC code.

| Control | Requirement | Validation |
|--------|-------------|-----------|
| **Budget bound** | No agent action may exceed a merchant-set cap without human approval. Proposed vs. cap is compared before execution. | Unit tests on `policy-engine.ts`; mock fixtures in `demo/lib/mock-data.ts`. |
| **Merchant gate** | Amount > merchant threshold ⇒ approval screen with audit trail; execution blocked until `{action_id, approved_by, approved_at}` recorded. | Flow test: approval required for > ₹2,000 fixture. |
| **Explainability** | Every recommendation must render `[✓]/[✗]` reason lines (action type allowed, budget ≤ cap, human approval needed). | Demo UI fixture + snapshot. |
| **Anomaly detection** | IsolationForest-style check flags unusual patterns before execution; flagged results require review. | Service unit test with synthetic anomaly. |
| **Reputation check** | Recipient/merchant reputation (GLEIF / Safe Browsing style) verified before payout. | Mock validator test. |
| **Idempotency** | Every payment carries `idempotency_key = SHA-256(action_id + merchant_id + amount + nonce)`; Redis atomic set lock prevents double-billing. | Unit test double-submit returns same result; no second charge. |
| **Non-custodial wallets** | OWS wallet private keys/seed phrases are injected via secrets only into the MCP wallet process, never into the agent process, never into frontend. | Static guard in CI blocks wallet `SECRET_KEY`/`SEED` usage outside `backend/mcp-servers/ows-mcp/`. |
| **Crypto rail** | USDC (x402) payments execute only through x402 gateway; output is signed; chain-of-custody logged. | Integration test against sandbox. |
| **Full-chain audit log** | Every action logs: what changed, who/what initiated (human vs agent), when started, evidence sources, decisions and rejections. | VPersuas-style log assertion in tests. |
| **KYC privacy** | Consumer KYC data encrypted at rest (AES-256); never logged in plaintext; anonymized in analytics signals. | Encryption unit test; log-scrub assertion. |
| **Secrets hygiene** | All API keys via environment variables only; `.env` never committed; `RAZORPAY_KEY_*`, `OWS_*`, `OPENROUTER_API_KEY`, `DATABASE_URL` only in server env. | Gitleaks + hardcoded-secret CI gate. |

---

## 6. Threat Definition Repository

Security definitions live under `security/definitions/<category>/ASDR-<NNN>-<slug>.yml` and follow the schema in `security/schemas/security-definition.schema.json`.

Each definition records: threat ID, name, category, severity, description, attack pattern, affected component/technology, detection indicators, detection method, preventive control, mitigation, validation procedure, status, first-observed, last-updated, revision history.

**Current definitions (all `active`):**

| ID | Category | Threat | Severity |
|----|----------|--------|----------|
| ASDR-001 | authentication | Exposed Credential | High |
| ASDR-002 | authorization | Broken Access Control | Critical |
| ASDR-003 | injection | Injection (prompt/command/SQL/NoSQL) | High |
| ASDR-004 | dependencies | Vulnerable Dependency / Supply Chain | High |
| ASDR-005 | data | Sensitive KYC/PII Data Exposure | Critical |
| ASDR-006 | infrastructure | Insecure Infrastructure & Secret Config | High |
| ASDR-007 | automation | Unsafe Automation (CI/agents) | High |
| ASDR-008 | availability | Availability Exhaustion (DoS) | Medium |
| ASDR-009 | finance | Agentic Payment Fraud (phantom/repeat intent) | Critical |
| ASDR-010 | finance | Wallet Key / Seed Exposure (crypto rail) | Critical |

New threats are added via the process in `security/README.md`; every new definition requires a detection rule, a mitigation runbook, and a validation procedure before it may become `active`.

---

## 7. Threat Lifecycle

```
Discovery → Classification → Definition → Validation → Integration
     → Automated Monitoring → Incident Detection → Mitigation
     → Verification → Definition Update → Historical Record
```

Definition status flow: `proposed → validated → active → updated → deprecated`. A definition is never activated merely because it looks plausible; it must be validated by the CI suite (`security/tests/validate_security.py`) and its rule must demonstrably fire.

---

## 8. Continuous Validation

### 8.1 Commit / Push Validation
On every push to `main`/`master`:
- Gitleaks secret scan (full history) + GitHub Secret Scanning.
- Hardcoded-credential pattern block (Razorpay keys, OpenRouter keys, GitHub PATs, private keys, JWT-style tokens, OWS wallet keys, mnemonic phrases).
- Workflow/config YAML integrity validation.

### 8.2 Pull-Request Validation
On every PR to `main`/`master`:
- All checks from 8.1.
- Dependency Review gate (`fail-on-severity: high`) — blocks PRs that introduce known-vulnerable or breaking dependency changes.
- CodeQL static analysis (JavaScript/TypeScript + Python).

### 8.3 Dependency Validation
- Dependabot monitors `demo/`, `app/`, `backend/` (npm + pip) and GitHub Actions daily/weekly.
- Because `backend/services/` and `backend/mcp-servers/` include Python, both `npm` and `pip` ecosystems are tracked.

### 8.4 Pre-Deployment Validation
Before merging a release, validate:
- Secrets present only in deployment env (Vercel/Railway/Render), never in the repo.
- Wallet material only in the OWS MCP process environment.
- Build succeeds (`next build` for `demo/` and `app/`); docker compose config parses.
- Security layer validation suite passes.
- 6-layer gate unit tests pass.

---

## 9. Security Testing

The repository ships a dependency-light validation suite, `security/tests/validate_security.py`, that runs locally (see `security/README.md`) and on CI. It verifies: required structure exists, all YAML parses, definitions carry required fields with valid enumerations, rules reference real definitions, incidents reference real definitions, and schema JSONs are valid.

This suite is executed by:
- `.github/workflows/security.yml` (push + PR)
- `.github/workflows/security-regression.yml` (weekly + manual dispatch)

---

## 10. Severity Classification

| Level | Meaning | Response |
|-------|---------|----------|
| Critical | Immediate financial/data risk (loss of funds, mass PII exposure) | Block merge & deploy; remediate immediately |
| High | Significant exploitable risk | Prioritized remediation before release |
| Medium | Moderate concern | Scheduled remediation |
| Low | Limited impact | Monitor |
| Informational | Improvement opportunity | Review during maintenance |

---

## 11. Security Regression Prevention

Every remediated vulnerability must produce a regression test (or a CI rule addition) so the weakness cannot be silently reintroduced:

```
Security Failure → Fix → Security Test → Automated Regression Check → Future Prevention
```

---

## 12. Incident Response

**Step 1 — Identify** the affected component (payment gate, wallet, API, dependency).
**Step 2 — Classify** severity (Section 10) and category.
**Step 3 — Contain** (revoke keys, disable webhook, freeze wallet, roll back deploy) — containing loss of funds takes precedence over everything.
**Step 4 — Remediate** (patch, rotate, blocklist).
**Step 5 — Validate** (run security suite + regression; verify payment/approval paths).
**Step 6 — Document** sanitized incident record in `security/incidents/` (no secrets, no PII).
**Step 7 — Update** definitions/rules with any reusable knowledge.
**Step 8 — Review** process effectiveness.

---

## 13. Security Reporting (Responsible Disclosure)

Do **not** open a public issue for a suspected vulnerability. Report privately:

- Via GitHub **Security Advisory / private vulnerability reporting** on `github.com/karun99/arthai`, or
- Directly to the maintainer.

Reports should include: description, affected component/endpoint, impact, reproduction steps (sanitized), suggested remediation, and evidence with secrets/PII removed. Maintainers commit to acknowledging disclosures within 7 days.

---

## 14. Roles & Responsibilities

- **Maintainers** — review security PRs, maintain workflows and definitions, respond to disclosures, rotate secrets, own release security gates.
- **Contributors** — follow secure coding practice, never commit secrets, run the validation suite locally before PR, flag risky changes.
- **Automation** — perform deterministic checks only; never bypass controls; report findings without exposing secrets/PII; never act autonomously on financial rails.
- **AI-assisted analysis** (S-AI, CodeQL suggestions) — assistance only; security-critical decisions stay deterministic + human-reviewed (Section 18 of the parent policy applies).

---

## 15. Security Metrics

Track: finding count, critical/high count, mean remediation time, dependency-vulnerability count, secret-scan events, security regressions, active definitions, validation pass/fail, unresolved incidents. Metrics improve posture; they do not prove absolute security.

---

## 16. Guardrails

1. Least privilege. 2. Secure defaults. 3. Defense in depth. 4. Fail closed on payments. 5. Validate before deploy. 6. Never store credentials in source. 7. Minimize sensitive data. 8. Keep dependencies updated. 9. Review third-party components (MCP servers are forked code — audit forks). 10. Audit everything by default. 11. Human review for high-impact actions. 12. Wallets non-custodial by default.

---

## 17. Limitations

This framework reduces risk; it does not eliminate it. Unknown vulnerabilities, business-logic flaws, human error, misconfigured external services, and novel attack techniques may evade automated detection. Per the adaptive principle: *continuous validation improves security posture but does not establish absolute security.*

---

## 18. Repository Security Structure

```
.github/
├── dependabot.yml                # daily/weekly dependency updates (npm + pip + actions)
└── workflows/
    ├── security.yml              # secret detection + hardcoded-secret block + config validation
    ├── codeql.yml                # CodeQL static analysis (js/ts + python)
    ├── dependency-review.yml     # PR gate on vulnerable dependencies
    ├── security-regression.yml   # weekly re-scan + rule self-test + validation suite
    └── validate-security-layer.yml # deterministic pass on the security layer itself

security/
├── README.md                     # layer navigation & contribution process
├── SECURITY_CHANGELOG.md         # versioned record of security-layer changes
├── definitions/                  # ASDR-001 … ASDR-010 (10 categories)
├── rules/                        # RULE-SEC-001 … RULE-SEC-005
├── mitigations/                  # MITIG-001 … MITIG-010 runbooks
├── incidents/                    # sanitized incident records
├── schemas/                      # definition + incident JSON schemas
└── tests/validate_security.py    # dependency-light validation suite

.env.example                      # variable template (placeholders only)
.gitignore                        # secret/credential exclusions
```

---

## 19. Continuous Defensive Cycle

```
Observe → Detect → Classify → Respond → Validate → Remember → Improve → (repeat)
```

The objective is not to claim immunity but to run a continuously improving defensive layer in which every detected threat produces reusable knowledge, a validated mitigation, and a regression control — on top of GitHub's native security stack.