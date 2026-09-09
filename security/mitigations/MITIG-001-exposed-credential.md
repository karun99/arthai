# MITIG-001 — Exposed Credential

**Threat:** ASDR-001 — Exposed Credential

## Steps

1. **Identify** which credential leaked and where (env, source, test fixture, history).
2. **Contain** — revoke immediately at the provider (Razorpay dashboard, OpenRouter, Supabase). Revoke beats rotate for suspected exposure.
3. **Rotate** — issue a new key, update only the deployment env (`vercel env`, Railway/Render service env).
4. **Purge** — remove the literal from every working copy and history (history rewrite only if repo is not widely forked yet; otherwise treat key as burned).
5. **Validate** — run `.github/workflows/security.yml` gitleaks + hardcoded-secret jobs locally against the full history; confirm zero matches.
6. **Prevent** — ensure the value never entered `.env.example`, lockfiles, or mock fixtures; add a new pattern to `RULE-SEC-001/002` if this shape was missed.

## Definition update
Record a sanitized incident (INC-*) and update `security/SECURITY_CHANGELOG.md`.