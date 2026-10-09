# OPSLY New Swarm: offline buyer-intent evidence tools

**This directory is outside the strict Division flow YAML source** located at
`opsly/buyer-intent-hunter`. It is a separate, no-spend Python standard-library
implementation. It does **not** use the legacy Opsly stack.

## Capabilities

- `collector.py`: optional approved-host HTTPS RSS collection with strict limits,
  no redirects and no network access until `--execute`; `sources.example.json`
  contains **no active sources**.
- `rss_adapter.py`: convert an already downloaded, permitted RSS/Atom XML
  file into candidate JSONL. It makes **no network calls**. It requires a
  published timestamp and an HTTPS evidence URL. It does not fabricate requests.
- `pipeline.py`: validate evidence fields, canonicalize HTTPS URLs, score
  German/English demand signals, discard promotional wording, mark stale
  items and deduplicate by URL and normalized text in local SQLite.
- `bridge.py`: select `review` candidates that have not been sent to the
  Division intake flow yet; **dry-run by default**. Only `--execute` performs
  authenticated event publication, with an explicit canonical bundle hash and
  `OPSLY_SWARM_API_TOKEN` secret read from environment. Acknowledgement is
  admission, **not** downstream completion, buyer verification or revenue.

## Approved feed collection (optional, disabled by default)

```bash
python3 -B collector.py \
  --sources sources.example.json \
  --out-dir /secure/feeds
```

This command only previews the configured feeds. After an authorized source list
has been completed and reviewed for public usage, `--execute` would allow
retrieval into local XML files; it never performs automatic discovery or outreach.

## Local offline flow

```bash
python3 -B rss_adapter.py \
  --xml-file /secure/feeds/permitted-feed.xml \
  --source-label permitted-public-feed \
  --output /secure/state/candidates.jsonl

python3 -B pipeline.py \
  --input /secure/state/candidates.jsonl \
  --db /secure/state/buyer-intent.sqlite

python3 -B bridge.py --db /secure/state/buyer-intent.sqlite
```

All example paths are operator-owned and are not deployed or created by this
README. The `--execute` bridge flag is **not** part of any scheduled job;
its prerequisites include a verified live deployment of
`opsly/buyer-intent-hunter` and an approved source/data-handling policy.

## No-spend testing

```bash
python3 -B -m unittest discover -s opsly/tools/buyer-intent/tests -v
go run ./cmd/swarm verify opsly/buyer-intent-hunter --portable
```

CI runs these on the `opsly/new-swarm` development branch, without any
database migration or deployment. Python tests use fixtures only; they are not
proof of real leads.

## Preconditions for live operation

1. Approve an actual public/legal RSS source and document its ToS and rate limits.
2. Confirm data retention/privacy policy for scraped public posts.
3. Verify the Division YAML contract and its persisted-event smoke test.
4. Ensure only one Render `swarm serve` holds the selected Postgres runtime store;
   rolling redeploys currently conflict with its exclusive advisory lock.
5. Protect the API with token; never store credentials in the repo.
6. Implement a production scheduler with observability, safeguards and source
   failure alerts. Nothing is currently scheduled here.
