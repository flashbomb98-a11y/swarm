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
    new_review = []
    with pipeline.connect_db(db_file) as db:
        db.execute('''CREATE TABLE IF NOT EXISTS daily_review_receipts (
            candidate_id TEXT PRIMARY KEY REFERENCES candidates(candidate_id),
            first_reported_at TEXT NOT NULL)''')
        stats = pipeline.ingest(prepared, db, now=now)
        with db:
            for item in prepared:
                try:
                    record = pipeline.prepare(item, now)
                except (ValueError, TypeError):
                    continue
                candidate_id, url, text, stamp, label, digest, score, bucket = record
                # Re-evaluate candidates even when a prior RSS summary lacked body text.
                db.execute('''UPDATE OR IGNORE candidates
                    SET request_text=?, discovered_at=?, source_label=?,
                        text_hash=?, score=?, bucket=?
                    WHERE candidate_id=? AND source_url=?''',
                    (text, stamp, label, digest, score, bucket, candidate_id, url))
                if bucket != 'review':
                    continue
                if not db.execute('''SELECT 1 FROM candidates
                    WHERE candidate_id=? AND source_url=?''', (candidate_id, url)).fetchone():
                    continue
                inserted = db.execute('''INSERT OR IGNORE INTO daily_review_receipts
                    (candidate_id, first_reported_at) VALUES (?, ?)''',
                    (candidate_id, now.isoformat()))
                if inserted.rowcount:
                    new_review.append({
                        'candidate_id': candidate_id, 'source_url': url,
                        'observed_at': stamp, 'source_label': label,
                        'score': score, 'status': 'UNVERIFIED - manual review required'
                    })
    new_review.sort(key=lambda item: (-item['score'], item['source_url']))
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
