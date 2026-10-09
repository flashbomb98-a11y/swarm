# Potential no-fee buyer-intent feed (NOT YET ENABLED)

External sources must be evaluated for terms, relevance, freshness and acceptable
use before they are placed into the actual feed configuration. The production
source registry defaults to `[]` and no scheduled web collection is active.

## Candidate A: Hacker News freelancer-request thread RSS

- Documented feed: https://hnrss.org/whoishiring/freelance
- Feed documentation: https://hnrss.github.io/
- Classification: public RSS feed of top-level comments in the recurring
  "Freelancer? Seeking freelancer?" Hacker News discussions.
- Business value: some entries may be project buyers, while others are
  freelancers advertising availability. Each entry must be categorized and
  verified before qualifying as purchase intent.
- Compliance: read public RSS conservatively, link to the original comment,
  never bulk message posters or bypass platform restrictions.
- Example **operator-review only** registry item (do not mistake for enabled
  automation):

```json
[
  {
    "label": "hn-freelance",
    "url": "https://hnrss.org/whoishiring/freelance",
    "approved_host": "hnrss.org"
  }
]
```

Inclusion in this document does not constitute evidence of any available buyer,
profit, permitted outreach or an operating collector. No network calls have
been made by the Opsly source collection code.

## Excluded by default

General remote employment RSS feeds mostly show hiring for employees rather
than buying agency services or projects. Do not conflate ordinary job vacancy
counts with verifiable buyer-intent for Opsly's sellable services.

## Enablement gates

Check current feed availability and publisher conditions; add to a private,
deployed source manifest after source-policy review; test no-redirect HTTPS
retrieval; schedule no faster than supported source usage and monitor
exceptions, duplicate rate, stale posts and actual qualified buyers.
