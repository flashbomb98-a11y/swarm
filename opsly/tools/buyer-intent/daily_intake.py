#!/usr/bin/env python3
"""Daily public-RSS buyer intent digest. No messages, API/LLM fees or buyer claims.

Network access requires --execute and an explicit allowlisted source manifest.
The public report deliberately excludes all original post text and personal data.
"""
import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import collector
import pipeline
import rss_adapter


def run(sources_file, db_file, output_file, *, execute=False, fetcher=None, now=None):
    sources = collector.load_sources(sources_file)
    if not execute:
        return {'mode': 'dry-run', 'sources': [f['label'] for f in sources],
                'network_calls': 0, 'outreach_sent': 0}
    if not sources:
        raise ValueError('no explicitly approved RSS sources configured')
    fetcher = fetcher or collector.retrieve
    now = now or datetime.now(timezone.utc)
    db_file = Path(db_file)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    prepared = []
    errors = []
    for source in sources:
        try:
            raw = fetcher(source)
            prepared.extend(rss_adapter.candidates(raw, source['label']))
        except (ValueError, OSError, UnicodeError) as exc:
            errors.append({'source': source['label'], 'error_type': type(exc).__name__})
    if errors:
        # A source outage must not generate a misleading clean/empty report.
        raise RuntimeError('source collection failed: ' + json.dumps(errors))
    with pipeline.connect_db(db_file) as db:
        previous = {r[0] for r in db.execute('SELECT candidate_id FROM candidates')}
        stats = pipeline.ingest(prepared, db, now=now)
        fresh = db.execute("""SELECT candidate_id,source_url,discovered_at,source_label,score,bucket
            FROM candidates WHERE bucket='review' ORDER BY score DESC, discovered_at DESC""").fetchall()
    new_review = [{'candidate_id': r[0], 'source_url': r[1], 'observed_at': r[2],
                   'source_label': r[3], 'score': r[4], 'status': 'UNVERIFIED - manual review required'}
                  for r in fresh if r[0] not in previous]
    result = {
        'run_at_utc': now.isoformat(),
        'mode': 'execute',
        'source_labels': [f['label'] for f in sources],
        'items_in_feed': len(prepared),
        'new_review_candidates': len(new_review),
        'statistics': stats,
        'leads': new_review[:100],
        'outreach_sent': 0,
        'revenue_claimed': 0,
        'notes': 'Heuristic review queue only. Links are public. Not verified buyers, no outreach.'
    }
    # Do not print or upload body texts, authors, emails, private fields or DB.
    output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return {'mode': 'execute', 'new_review_candidates': len(new_review),
            'items_in_feed': len(prepared), 'outreach_sent': 0,
            'report': str(output_file)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sources', required=True)
    p.add_argument('--db', required=True)
    p.add_argument('--report', required=True)
    p.add_argument('--execute', action='store_true')
    args = p.parse_args()
    print(json.dumps(run(args.sources, args.db, args.report, execute=args.execute)))


if __name__ == '__main__':
    main()
