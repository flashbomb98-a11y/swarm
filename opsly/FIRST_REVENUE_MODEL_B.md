# Opsly: first-revenue plan — Service model B

**Decision: 2026-10-09. This is the active commercial direction until a real paid pilot validates it.**

## Goal

Earn the first **real, documented service payment**, not commissions from reselling leads. The first target is one paid client, then three repeatable orders. No revenue is claimed yet.

## One initial product: "Webseiten-Schnellstart"

- **Customer:** a self-employed professional or small local service business publicly requesting a simple landing page.
- **Offer:** one responsive single-page business website, clear service sections, contact call-to-action, mobile layout, basic title/description metadata and one correction round.
- **Introductory fixed price:** EUR 349 per project (price hypothesis, not validated).
- **Delivery target:** roughly three business days *after* receipt of all agreed assets and access; no unconditional deadline promise.
- **Payment:** propose a written scope and invoice, 50% deposit before production, remainder on acceptance. Customer handles domain/hosting fees separately.
- **Excluded:** complex e-commerce, custom software, paid ads, maintenance, bespoke branding, stock photography licenses, regulated/guaranteed SEO, or legal drafting. Customer supplies rights-cleared images and correct legal/privacy content.

## How Division Swarm fits

The **existing Division Swarm architecture** is the workflow authority. The fork `flashbomb98-a11y/swarm` contains `opsly/buyer-intent-hunter` as a verified deterministic *intake*, plus feed collection, scoring and deduplication tooling. Those are not proof of real buyer leads or orders.

Desired journey:
1. Collect only permitted, public expressions of an explicit project need (evidence URL, timestamp, source rules).
2. Exclude people looking for work, irrelevant vacancies, suppliers pitching services, stale notices, and requests needing substantial custom software.
3. Put matching website/landing-page requests into a human review queue with citation and source link.
4. Check that a response is allowed on the source platform and that the request is still open.
5. Prepare a **human-approved, individualized response**. No automatic cold messages or mass outreach.
6. Confirm scope, deliver the site using simple reusable templates, obtain acceptance and invoice correctly.

## First 14-day commercial validation

- Prepare **one fictional, clearly labeled demonstration** of the landing-page service; no fake testimonials or client claims.
- Produce 10 genuinely relevant, current, individually verifiable opportunities; zero is a valid outcome and signals we need better permitted sources.
- Respond manually to up to five expressly open requests where platform terms permit.
- Track replies, discovery calls, quotes, deposits and actual receipts. Do not promise conversion.
- Pause expansion if the source feed mostly contains freelancers seeking work or job ads.

## Truthful status and guardrails

- Revenue as of this plan: **not verified**.
- The running Render `division-swarm-final-postgres` still runs an **upstream sample flow**, not this buyer-intent business flow.
- The GitHub daily report has run, but forwarding into the actual Swarm runtime is disabled by default. Do not describe the end-to-end pipeline as live.
- No production cutover, paid API, external messaging, database reset, extra infrastructure or secret transfer without explicit authorization.
- Any future changes belong on the fork/development branch, follow existing Division Swarm YAML contracts and pass tests before release.
- Prioritize **first real sale and simple delivery** over additional agents, dashboards or infrastructure.

## Success criteria

Success is **one actually paid EUR 349 project delivered and accepted**, verified via normal business records, not a synthetic test, a green CI job, or a count of scraped links. The seller remains responsible for legal, tax, customer and platform obligations.
