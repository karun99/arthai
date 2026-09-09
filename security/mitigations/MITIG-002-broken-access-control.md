# MITIG-002 — Broken Access Control

**Threat:** ASDR-002 — Broken Access Control

## Steps

1. **Contain** — if the surface is money-moving (approval/payment/webhook), freeze the endpoint (revoke deploy or feature-flag it off). This takes priority.
2. **Identify** the route/tool and the missing check (authn, role, ownership, signature verification).
3. **Fix**
   - Add role guard middleware; every finance route requires `vendor`/`admin` role.
   - Validate Razorpay `X-Razorpay-Signature` with the webhook secret before processing events.
   - Scope MCP tools by role allowlist in the server config; never register a tool without a role annotation.
   - Ownership-check every object read (`resource.ownerId === session.id`).
4. **Validate** — add/adjust authorization tests: unauthenticated → 401/403; forged webhook → rejected; cross-tenant access → denied.
5. **Regression** — keep the new tests permanent; code-review checklist gains a mandatory "role check present on this route?" line.

## Definition update
Record incident; update `ASDR-002` status/observations if a new bypass shape was found.