# MITIG-006 — Insecure Infrastructure & Secret Configuration

**Threat:** ASDR-006 — Insecure Infrastructure & Secret Configuration

## Steps

1. **Contain** — close exposed ports; rotate any default credentials (Redis/Postgres/Neo4j/ChromaDB) and any secrets found in compose/env files.
2. **Identify** the insecure definitions: compose files with literals, public bindings, root containers, default auth.
3. **Fix**
   - Move all secrets out of files: use orchestrator env (Vercel/Railway/Render secrets), Docker secrets, or service env at runtime.
   - Bind data stores to the internal backend network only (no `0.0.0.0` for 6379/7687/7474/9080).
   - Run containers as non-root; mount wallet dirs read-only.
   - Require authentication on every data store; rotate credentials at first deploy.
4. **Validate** — `docker compose -f backend/docker-compose.yml config` parses with zero secrets; CI grep gate blocks secret literals in infra files; containers declare `security_opt`/non-root for wallet services.
5. **Regression** — infra diff checklist before every release; scheduled port-binding scan.

## Definition update
Record INC; update `ASDR-006` if a new misconfiguration class was found.