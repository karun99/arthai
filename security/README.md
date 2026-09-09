# Adaptive Security Layer — ArthAI

Reusable, financial-grade threat definitions, detection rules, mitigations, and
incident history for **ArthAI** (`github.com/karun99/arthai`). Driven by
`SECURITY_POLICY.md` and automated by `.github/workflows/`.

## Layout

```
security/
├── SECURITY_CHANGELOG.md     # versioned record of changes (this layer)
├── definitions/              # threat definitions (ASDR-*), one per category
│   ├── authentication/       #   ASDR-001  Exposed Credential
│   ├── authorization/        #   ASDR-002  Broken Access Control
│   ├── injection/            #   ASDR-003  Injection
│   ├── dependencies/         #   ASDR-004  Vulnerable Dependency / Supply Chain
│   ├── data/                 #   ASDR-005  Sensitive KYC / PII Data Exposure
│   ├── infrastructure/       #   ASDR-006  Insecure Infrastructure / Secret Config
│   ├── automation/           #   ASDR-007  Unsafe Automation
│   ├── availability/         #   ASDR-008  Availability Exhaustion
│   └── finance/              #   ASDR-009  Agentic Payment Fraud
│                             #   ASDR-010  Wallet Key / Seed Exposure
├── rules/                    # detection rules (RULE-SEC-*), enforced by CI
├── tests/                    # deterministic validation scripts
├── mitigations/              # runbooks for each threat (MITIG-*)
├── incidents/                # sanitized incident records (INC-*)
└── schemas/                  # JSON schemas for definitions & incidents
```

## Governance

- **Policy** — `SECURITY_POLICY.md` (v1.0) defines objectives, the mandatory
  6-layer financial gate, lifecycle, severity, and incident response.
- **Automation** — `.github/workflows/{security,codeql,dependency-review,security-regression,validate-security-layer}.yml`
  plus `.github/dependabot.yml`.
- **Validation** — run `python3 security/tests/validate_security.py` locally;
  the same checks run on every push/PR and on the weekly regression.

## Adding a threat

1. Create `security/definitions/<category>/ASDR-<NNN>-<slug>.yml` following
   `security/schemas/security-definition.schema.json`.
2. Add a detection rule `security/rules/RULE-SEC-<NNN>.yml` referencing the ID.
3. Add a mitigation runbook `security/mitigations/MITIG-<NNN>-<slug>.md`.
4. Update `security/SECURITY_CHANGELOG.md` and validate with the test suite.
   A definition becomes `active` only after the suite passes and the rule is
   demonstrably enforced in CI.

## Financial gate

Every change touching payments, wallets, or KYC must keep the 6-layer gate
intact (see `SECURITY_POLICY.md` §5): **bounded → gated → explainable →
anomaly → reputation → audit**. The layer verifies these control points stay
present via tests and CI gates; it does not enforce the gate at runtime —
`app/lib/policy-engine.ts` does.