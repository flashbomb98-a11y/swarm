# New OPSLY Division Swarm — production cutover gates

_Status checked 2026-10-09. This is a **runbook**, not approval or proof that production is live._

## Scope isolation

Only the fork `flashbomb98-a11y/swarm` and the new Division Swarm infrastructure are in scope. Do not connect old Floot/Market agents or their data.

## State discovered

| Component | Current evidence | Go-live rule |
| --- | --- | --- |
| New workflow | `opsly/buyer-intent-hunter`, verified via dedicated CI | Must pass static and synthetic runtime tests |
| Evidence tools | `opsly/tools/buyer-intent`, standard-library Python | Unit tests; authorized sources; no secrets in repo |
| Render active candidate | `division-swarm-final-postgres` is wired to upstream `division-sh/swarm`, not our fork | Change source in the Render dashboard only after verified single-owner plan |
| Render PostgreSQL | `division-swarm-pg16`, free PG16, available in Oct 9 read; expires 2026-11-08 | Backup and replacement decision well before expiry, **no automatic paid upgrade** |
| Separate Neon PostgreSQL | `division-swarm-state`, schema already present | Keep distinct. Do **not** swap into Render via guesswork |
| Railway drafts | `Division Swarm Basement`, `Agent Zero Basement`, staged only | Do not deploy empty templates |

## Blocking ownership handover

Render logs show a successful boot with PostgreSQL store, followed by a failed overlapping deploy: `startup ownership lease · Another swarm serve is already running for this project`. Its Go runtime holds a PostgreSQL advisory lock for one active serving instance. Blind restart, clearing a database, repairing authority, or re-deploying in a loop is **not a fix**.

Before switching source: verify the actual active runtime and its store; take a safe snapshot/backup; choose a controlled shutdown-first cutover that does not start another `swarm serve` against the still-owned store. Plan downtime, rollback and health readback. Make no destructive or fee-bearing action without explicit approval.

## Validation and evidence requirements

1. GitHub Actions dedicated workflow on the development branch: `go run ./cmd/swarm verify opsly/buyer-intent-hunter --portable`, plus synthetic fixture `go run ./cmd/swarm test opsly/buyer-intent-hunter` and 21 Python tests.
2. Confirm `intent.candidate.received` is accepted, `intent.review.queued` is actually emitted and persisted. A passing static check is **not** persistent runtime proof.
3. Admit only genuine HTTPS evidence, timestamp, source URL and source policy; dedupe by URL and content. All items have `evidence_status=unverified`.
4. The optional bridge to JSON-RPC is **dry-run by default** and requires a canonical live bundle hash and secret token plus `--execute`; no automatic outreach.
5. Configure actual permitted public feed sources before enabling scheduled discovery; no crawling or posting without compliance review.
6. Place monitoring around stale feeds, accepted events, queue lag, retries, runtime restarts and expired source credentials.
7. Check Render running deployment, API response and persistent database readback after an approved cutover. On any failure, roll back without resetting the database.

## Human gates

A single human approval is still required for any production interruption/cutover, paid provider usage, platform login, DNS/account linking, secrets entry, and committing to real outreach or payment. The code branch can proceed through static tests without those approvals.

## Explicitly not complete

No live scheduled permitted source discovery, no real verified buyers, no paid LLM reviewer, no proven Render cutover or end-to-end production event persistence. Do not present these as complete until evidence is collected.
