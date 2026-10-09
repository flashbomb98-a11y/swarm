# OPSLY – NEW Division Swarm (independent project)

**This is the NEW build. Do not reconnect legacy Opsly Market, Floot Command
Center, Cash CEO or other deprecated agents.**

### Source layout

- [Buyer intent flow](buyer-intent-hunter/) – Division YAML, root ingress
  `intent.candidate.received`, durable event `intent.review.queued`;
  successful intake means recorded request, **not** verified lead.
- [Buyer intent tools](tools/buyer-intent/) – zero-fee Python standard library
  tools: optional allowlisted RSS collector, RSS/Atom parser, deterministic
  scoring and SQLite dedupe, opt-in authenticated Division RPC bridge.
- [Render launch preparation](deploy/render/start.sh) – fail-closed start
  launcher; **never use during an overlapping render deployment**.
- [Source candidates](POTENTIAL_PUBLIC_SOURCES.md) – research only, no source
  activated by default.
- [State and boundaries](NEW_SWARM_BOUNDARIES.md) and
  [production cutover runbook](PRODUCTION_CUTOVER_RUNBOOK.md).

### Automated verification

Dedicated workflow:
[OPSLY isolated checks](../.github/workflows/opsly-new-swarm.yml)

- Division static verification: passed.
- Synthetic event scenario: passed via `swarm test`.
- 28 Python standard-library tests: passed on GitHub Actions
  [run #17](https://github.com/flashbomb98-a11y/swarm/actions/runs/37923162637).
- Render fail-closed launcher preflight: checked separately (no service started).

**No production deployment or paid API calls were performed by these commits.**

### Operational status

The code is a **tested development foundation**, not a fully autonomous revenue
swarm. No live sources, verified paying buyers, outreach or scheduled workflow
have been demonstrated. The existing Render service is still wired to upstream
`division-sh/swarm` and its PostgreSQL store is subject to an exclusive
single-process runtime lock that caused overlapping deploy failures.

Before production cutover: source approval, persistent scheduler, credentials,
a controlled shutdown-first handover, database backup/expiry plan and real
event/readback verification are required. Do not blindly re-deploy, restart,
suspend or repair authority.
