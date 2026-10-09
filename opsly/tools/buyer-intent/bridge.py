#!/usr/bin/env python3
"""Safe opt-in handoff of queued evidence to a correctly deployed Division Swarm runtime.

Dry-run by default. --execute requires HTTPS, an explicit bundle hash and a secret
from the environment. API acknowledgement is not a qualification or sale.
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlsplit

BUNDLE = re.compile(r'^bundle-v2:sha256:[a-f0-9]{64}$')


def publication(candidate, bundle_hash):
    candidate_id, source_url, text, discovered_at, source_label = candidate
    if not BUNDLE.fullmatch(bundle_hash):
        raise ValueError('a canonical runtime bundle_hash is required')
    return {'jsonrpc': '2.0', 'id': candidate_id, 'method': 'event.publish',
            'params': {'bundle_hash': bundle_hash,
                       'event_name': 'intent.candidate.received',
                       'payload': {'candidate_id': candidate_id, 'source_url': source_url,
                                   'request_text': text, 'discovered_at': discovered_at,
                                   'source_label': source_label},
                       'idempotency_key': 'opsly-intake:' + candidate_id}}


def candidates(db, limit):
    return db.execute('''SELECT candidate_id,source_url,request_text,discovered_at,source_label
        FROM candidates WHERE bucket='review' AND candidate_id NOT IN
        (SELECT candidate_id FROM bridge_receipts) ORDER BY discovered_at DESC LIMIT ?''', (limit,)).fetchall()


def ensure_receipt_table(db):
    db.execute('''CREATE TABLE IF NOT EXISTS bridge_receipts (
        candidate_id TEXT PRIMARY KEY REFERENCES candidates(candidate_id),
        accepted_at TEXT NOT NULL,
        response_json TEXT NOT NULL)''')


def publish(api_url, bearer, payload, timeout=15):
    url = urlsplit(api_url)
    if url.scheme != 'https' or not url.hostname or url.username or url.password or url.query or url.fragment:
        raise ValueError('authenticated control API must use a direct HTTPS base URL')
    if not bearer:
        raise ValueError('empty bearer credential')
    request = urllib.request.Request(api_url.rstrip('/') + '/v1/rpc',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bearer},
        method='POST')
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read(100_000).decode('utf-8'))
        if not isinstance(body, dict) or 'error' in body or 'result' not in body:
            raise ValueError('runtime refused event publication')
        return body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True)
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--bundle-hash', default='')
    parser.add_argument('--api-url', default='')
    parser.add_argument('--execute', action='store_true', help='Actually publish events: opt-in only')
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error('--limit must be 1..100')
    with sqlite3.connect(args.db) as db:
        ensure_receipt_table(db)
        selected = candidates(db, args.limit)
        if not args.execute:
            print(json.dumps({'mode': 'dry-run', 'would_publish': len(selected),
                              'candidate_ids': [row[0] for row in selected]}))
            return
        if not BUNDLE.fullmatch(args.bundle_hash) or not args.api_url:
            parser.error('--execute requires --bundle-hash and --api-url')
        bearer = os.environ.get('OPSLY_SWARM_API_TOKEN', '')
        accepted = 0
        for row in selected:
            try:
                body = publish(args.api_url, bearer, publication(row, args.bundle_hash))
            except (ValueError, urllib.error.URLError, TimeoutError) as exc:
                # Never log bearer secrets or raw request contents.
                print('Submission failed for candidate ' + row[0] + ': ' + type(exc).__name__, file=sys.stderr)
                break
            with db:
                db.execute('INSERT OR IGNORE INTO bridge_receipts VALUES (?,?,?)',
                           (row[0], datetime.now(timezone.utc).isoformat(), json.dumps(body)))
            accepted += 1
        print(json.dumps({'mode': 'execute', 'accepted_for_dispatch': accepted,
                          'requested': len(selected)}))


if __name__ == '__main__':
    main()