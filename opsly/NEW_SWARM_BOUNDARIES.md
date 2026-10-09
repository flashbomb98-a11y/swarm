# NEW Division Swarm — project boundaries and technical baseline

As of 2026-10-09. Only the new Division Swarm project is in scope. **Do not reuse** old Opsly Market, old Floot Command Center, legacy Cash CEO / Seller agents or historic "Buyer Intent Hunter" automations.

## Verified infrastructure

- Own fork: `flashbomb98-a11y/swarm`, development branch `opsly/new-swarm`.
- Framework: `division-sh/swarm`, platform spec 0.7.0; upstream Apache 2.0.
- Render workspace: `Opsly's workspace`.
- Render primary candidate: `division-swarm-final-postgres`, source currently upstream `division-sh/swarm`, not this fork. Build succeeded in earlier run; newer startup failed with `startup ownership lease · Another swarm serve is already running`.
- Render Postgres `division-swarm-pg16`: available, **free** plan, expiration shown 2026-11-08. External read-only SQL access from current connector is blocked by its networking allowlist. No claims about current table contents.
- Neon `division-swarm-state`: separate external PostgreSQL; contains Division Swarm schema but no recorded agents / event runs during 2026-10-09 read check. Do not assume that it is the Render service's active database.
- Railway `Division Swarm Basement` and `Agent Zero Basement`: staged resources only, never deployed. They are not the active Render production system.
- A control probe logged `ready=true, db_ok=true` against an earlier version of the runtime. That is not proof the failed latest deploy or actual business agents work.

## Operating rules

1. No new paid services, upgrades or metered LLM API use without explicit approval.
2. Do not restart, suspend, delete, reset or migrate production databases just to resolve uncertainty.
3. Do not publish customer outreach automatically. Verify buyer intent and follow source rules.
4. Avoid duplicate runtime ownership: rolling deployments may overlap and cause Postgres advisory lock conflict.
5. Ensure tokens and passwords remain in secret environment settings only; never commit them.
6. Verify deployments and live behavior through logs, readback and actual persisted events before saying "running".
7. Start with deterministic intake and evidence traceability, expand into authentic source discovery, deduplication and human-reviewed outreach only after proof.
8. All new code belongs on the fork and a development branch. Do not alter upstream or old Opsly products.

## Rollout sequence

1. Verify isolated intake contract with `swarm verify`.
2. Add test harness for persisted intake and replay using an isolated SQLite store.
3. Implement permitted discovery adapters and deterministic quality scoring with reference/evidence provenance.
4. Add isolated AI reviewer and usage/cost ceilings, only with user-approved LLM budget.
5. Prepare PostgreSQL backup, single-owner Render deployment strategy, health checks and credential review.
6. Cut over after explicit cost/deployment review and prove end-to-end candidate intake, dedupe, triage and persisted results.

**Completion status: initial source-controlled contract, not end-to-end live system.**

## Verified progress on 2026-10-09

- Division contract source: `opsly/buyer-intent-hunter` (YAML declarations only). `intent.candidate.received` -> `intent.review.queued` -> terminal intake state. This is a deterministic **intake**, not an implemented commercial reviewer.
- Separate no-network / no-fee tools: `opsly/tools/buyer-intent`. Local RSS/Atom XML -> JSONL, local SQLite dedupe and deterministic scoring, opt-in secure JSON-RPC bridge with dry-run default, token in environment only.
- Dedicated GitHub Actions workflow: `.github/workflows/opsly-new-swarm.yml`. **Verified successful run 37922549651**: `swarm verify --portable` passed, `swarm test` reported `scenario ok: tests/visible-smoke.yaml` and `scenarios=1`, and 21 Python tests passed. https://github.com/flashbomb98-a11y/swarm/actions/runs/37922549651
- Code tested on dev branch `opsly/new-swarm` only; no deployment/merge has occurred.
- Current safety: all buyer evidence remains unverified and outreach not sent. Test fixture is explicitly synthetic; no production buyer discovery or business sales verified.

**Remaining blockers:** live allowed source registration/permissions, persistent feed scheduler and alerting, approved LLM costs (if using LLM-based scoring), Render change from upstream GitHub repo to own fork, single-owner PostgreSQL cutover and independent live event readback, Render free database expiry/backup. None of those is proven operational by CI.

## Latest full regression verification (2026-10-09)

- Source-controlled optional, allowlisted HTTPS RSS collector; `sources.example.json` remains `[]`. No public feed has been fetched or scheduled.
- Evidence JSONL, SQLite, XML, .env, secrets and caches are ignored in the public repository under `opsly/tools/buyer-intent/.gitignore`.
- Safe Render launcher `opsly/deploy/render/start.sh` has been checked for Bash syntax and refuses to start when DB_HOST or other required variables are missing. It was **not deployed or executed against a database**.
- GitHub CI [run 37923437596](https://github.com/flashbomb98-a11y/swarm/actions/runs/37923437596) passed all four steps: Render launcher dry preflight, Division `verify --portable`, synthetic `swarm test` (`scenarios=1`), Python tests (`28 tests, OK`).
- No real customer requests, payments, scheduled feed polling or production event processing are claimed.
- Next: approved data source, dedicated persistent scheduler, single-owner Render fork cutover after real backup and user approval, production API integration/readback; Render free PostgreSQL expires 2026-11-08.
