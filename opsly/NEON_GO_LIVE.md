# NEW Opsly Buyer Intent Hunter — isolated, no-paid-upgrade Go-Live

This is the **new** Opsly Division Swarm only. No legacy Market/Floot agent
or database is used.

## Prepared deployment

The repository-root [render.yaml](../../render.yaml) was verified against the
official Render Blueprint layout. It describes **one** new Go web service:

- Render name: `opsly-new-buyer-intent`
- Plan: `free`; region: `frankfurt`; branch: `master`
- Build: `go build -o swarm ./cmd/swarm && go build -o opsly-portgate ./opsly/deploy/render/cmd/portgate`
- Start: `bash opsly/deploy/render/start.sh`
- Health: `/_opsly/gate/ready` (503 until the Swarm backend is listening)
- External Postgres: **existing Neon `division-swarm-state`**, database
  `neondb` with **direct** host, NOT transaction pooler
- One mandatory secret: `DB_PASSWORD`, entered by the operator directly in
  Render's *initial Blueprint creation* prompt (`sync: false`)
- `SWARM_API_TOKEN` is generated securely by Render, not committed.
- Does not define a new database, disk, upgrade or any paid plan.

One-click blueprint source:
https://render.com/deploy?repo=https://github.com/flashbomb98-a11y/swarm

Before confirming, check the preview: **one new FREE web service only** and
no database. Cancel if that is not what Render displays, or if it requests a
paid upgrade.

### Secret provisioning

Get the existing Neon database password from https://console.neon.tech/
for project `division-swarm-state`. Paste it into Render's secure
`DB_PASSWORD` field. Never send the password by chat or commit it to GitHub.

Credentials are currently the **one unavoidable operator-only step**.
The connected Render service-management API in this chat cannot set source,
branch, build command or start command on an existing service. A prior attempt
to cross-copy privileged Neon credentials between connectors was blocked, and
must not be retried via an insecure workaround.

### Readback gates before claiming production success

1. Render shows one **live** service with the correct name and fork repository.
2. Render logs show the internal `swarm serve opsly/buyer-intent-hunter`
   backend started with `postgres` and no advisory lock refusal.
3. Probe `https://opsly-new-buyer-intent.onrender.com/_opsly/gate/ready`
   returns 200 after waking the Render Free instance.
4. Through authenticated `/v1/rpc`, publish a synthetic
   `intent.candidate.received` event and prove persistence/readback in
   **the correct Neon database**.
5. Verify the new input event and `intent.review.queued` are durably
   recorded. Never report synthetic test records as real buyers.
6. Enable authenticated GitHub Actions -> Division RPC forwarding only after
   confirming the canonical runtime bundle hash, source/privacy policy and
   securely provisioning GitHub credentials. The workflow's optional publication
   stage is implemented but DISABLED by default. GitHub repository settings:
   Actions variable `OPSLY_ENABLE_RPC_PUSH=true` (only after verification),
   variables `OPSLY_SWARM_URL` and `OPSLY_SWARM_BUNDLE_HASH`, and secret
   `OPSLY_SWARM_API_TOKEN` matching Render's generated token. Never commit the
   bearer token or put it in a public issue. The collector works independently
   before this toggle; unverified evidence enters review, never outreach.
7. Confirm acceptable source usage, data retention, backlog and alerting.
8. Verify cost-free status and plan for free-tier sleeping/quotas. Render Free
   cannot guarantee nonstop 24/7 compute.

### Already verified

- The daily GitHub Actions public RSS feed collector runs and emits review
  reports; no outreach.
- Division YAML contract, scenario smoke and 35 Python tests have passed.
- Render `portgate` has its own Go package tests and builds successfully.
- The Neon project has been checked and there are no current advisory locks
  or recorded runtime events (at time checked 2026-10-09).
- None of these guarantees a *production* deployment. It is not live until
  the readback gates pass.
