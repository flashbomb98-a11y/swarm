# New Swarm: Buyer Intent intake (v0.1.0)

This is **only the first deterministic contract for our new project**. It is not the old Opsly/Market system. It deliberately has **zero LLM agents** and makes **zero third-party calls**, so no external spend can arise from executing the contract itself.

## What works by design

A caller submits a genuinely observed buyer request with a stable candidate ID, original source URL, verbatim request text, timestamp and source label. The durable runtime records the incoming event, emits `intent.review.queued`, and advances the flow to `done` to indicate **intake was completed**, not that the lead was qualified or contacted.

All payload values come from the caller. No data, buyer or sale is invented by the workflow. The events form an auditable hand-off to a future evaluation agent.

## Verify locally against the fork

```bash
go build -o swarm ./cmd/swarm
./swarm verify opsly/buyer-intent-hunter --portable
```

Start this *only in a separate development runtime* (SQLite is the default); **do not** point a second `swarm serve` instance to the existing Render production PostgreSQL store because Division Swarm requires exclusive runtime ownership.

```bash
./swarm serve opsly/buyer-intent-hunter --dev --api-listen-addr 127.0.0.1:8081
./swarm event publish intent.candidate.received --payload-json '{"candidate_id":"test-only-001","source_url":"https://example.org/test-only","request_text":"Synthetic development fixture, not a real buyer request","discovered_at":"2026-10-09T12:00:00+02:00","source_label":"test-fixture"}'
```

The example is a synthetic **test**, not a commercial opportunity.

## Not yet implemented / go-live gates

- No real source connector, scheduled discovery, or authorized crawling yet.
- No intent scoring, deduplication, evidence freshness rules, review agent or outbound outreach yet.
- No secure LLM credentials, usage caps or provider-cost approval.
- No deployment on production Render, because its current runtime has a verified overlapping-deployment PostgreSQL ownership conflict.
- No payment, prospect message or external service action may be performed without separate authorization.

## Deployment safety

GitHub changes stay on `opsly/new-swarm`; `master`, old Floot Opsly projects, Railway drafts, Render services and both databases are untouched. Before any production cutover: verify contract, prove test event persistence in an isolated store, add actual discovery/qualification components, fix runtime single-owner deployment strategy, back up data and secure the API.

See `opsly/NEW_SWARM_BOUNDARIES.md`.
