#!/usr/bin/env python3
"""Offline, no-spend buyer-intent intake. No network calls or outbound actions."""
import argparse
import hashlib
import ipaddress
import json
import re
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

REQUIRED = ('candidate_id', 'source_url', 'request_text', 'discovered_at', 'source_label')
BUYER_SIGNALS = (
    (r'\b(?:looking for|seeking|need (?:a |an |someone |help |to )|hiring|can anyone recommend)\b', 45),
    (r'\b(?:suche|gesucht|ben[oö]tige|brauche|beauftragen|wer kann|hat jemand einen tipp)\b', 45),
    (r'\b(?:budget|paid|paying|quote|quotation|angebot|auftrag|verg[uü]tung)\b', 25),
    (r'\b(?:asap|urgent|this week|diese woche|dringend|sofort|deadline)\b', 12),
)
PROMOTION = re.compile(r'\b(?:we offer|our services|buy my|discount|promo code|ich biete|wir bieten|jetzt kaufen|verkaufe)\b', re.I)
# Posts by providers looking for work are not requests from paying buyers.
# The source's "SEEKING WORK" entries must never become customer leads.
SUPPLIER_REQUEST = re.compile(
    r"(?im)^\s*(?:\[[^\]\n]{1,40}\]\s*)?"
    r"(?:(?:i'm|i am|we're|we are|freelancer|developer|designer)\s+)?"
    r"(?:seeking\s+(?:work|clients?|contracts?|projects?|employment)|"
    r"looking\s+for\s+(?:work|jobs?|clients?|contracts?|projects?)|"
    r"(?:available|open)\s+(?:for|to)\s+(?:hire|work)|"
    r"for\s+hire|"
    r"suche\s+(?:arbeit|jobs?|kunden|auftr[aä]ge)|"
    r"biete\s+(?:meine\s+)?(?:dienste|dienstleistungen)\s+an)\b"
)
TRACKING = {'fbclid', 'gclid', 'msclkid', 'ref_src'}


def canonical_url(raw):
    """Normalize dedupe key without fetching the URL; reject private/link-local IPs."""
    parsed = urlsplit(raw.strip())
    if parsed.scheme.lower() != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('source_url must be a public HTTPS URL without credentials')
    host = parsed.hostname.lower()
    if host == 'localhost' or host.endswith('.local'):
        raise ValueError('local URLs are not evidence')
    try:
        if not ipaddress.ip_address(host).is_global:
            raise ValueError('non-public IP URLs are not evidence')
    except ValueError as exc:
        if 'not evidence' in str(exc):
            raise
    if parsed.port and parsed.port != 443:
        raise ValueError('non-default HTTPS port not accepted')
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
                             if not k.lower().startswith('utm_') and k.lower() not in TRACKING))
    path = parsed.path.rstrip('/') or '/'
    return urlunsplit(('https', host, path, query, ''))


def parse_timestamp(raw, now):
    dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError('discovered_at requires an explicit timezone')
    if dt > now + timedelta(minutes=5):
        raise ValueError('discovered_at is in the future')
    return dt.astimezone(timezone.utc)


def score_intent(text, discovered_at, now):
    """Deterministic heuristic; human verification is always required."""
    if PROMOTION.search(text):
        return 0, 'reject_promotion'
    if SUPPLIER_REQUEST.search(text):
        return 0, 'reject_supplier'
    score = sum(weight for regex, weight in BUYER_SIGNALS if re.search(regex, text, re.I))
    age = now - discovered_at
    if age > timedelta(days=30):
        return min(score, 40), 'stale'
    if age > timedelta(days=7):
        score = max(0, score - 15)
    score = min(score, 100)
    return score, 'review' if score >= 45 else 'watch'


def prepare(item, now):
    if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip() for k in REQUIRED):
        raise ValueError('candidate must provide five nonempty string fields')
    if len(item['request_text']) > 10000 or len(item['candidate_id']) > 200 or len(item['source_label']) > 200:
        raise ValueError('candidate field exceeds length limit')
    link = canonical_url(item['source_url'])
    observed = parse_timestamp(item['discovered_at'], now)
    score, bucket = score_intent(item['request_text'], observed, now)
    # Content digest also detects the same request mirrored at another URL.
    digest = hashlib.sha256(re.sub(r'\s+', ' ', item['request_text'].casefold()).strip().encode()).hexdigest()
    return (item['candidate_id'].strip(), link, item['request_text'].strip(),
            observed.isoformat(), item['source_label'].strip(), digest, score, bucket)


def connect_db(path):
    db = sqlite3.connect(str(path))
    db.execute('PRAGMA foreign_keys=ON')
    db.execute('''CREATE TABLE IF NOT EXISTS candidates (
        candidate_id TEXT PRIMARY KEY,
        source_url TEXT NOT NULL UNIQUE,
        request_text TEXT NOT NULL,
        discovered_at TEXT NOT NULL,
        source_label TEXT NOT NULL,
        text_hash TEXT NOT NULL UNIQUE,
        score INTEGER NOT NULL,
        bucket TEXT NOT NULL,
        evidence_status TEXT NOT NULL DEFAULT 'unverified',
        outreach_status TEXT NOT NULL DEFAULT 'not_sent',
        CHECK (score BETWEEN 0 AND 100)
    )''')
    return db


def ingest(items, db, now=None):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('now must be timezone-aware')
    stats = {'inserted': 0, 'duplicates': 0, 'invalid': 0, 'review': 0, 'watch': 0, 'stale': 0, 'reject_promotion': 0, 'reject_supplier': 0}
    with db:
        for item in items:
            try:
                record = prepare(item, now)
                result = db.execute('''INSERT OR IGNORE INTO candidates
                    (candidate_id,source_url,request_text,discovered_at,source_label,text_hash,score,bucket)
                    VALUES (?,?,?,?,?,?,?,?)''', record)
                if result.rowcount == 0:
                    stats['duplicates'] += 1
                else:
                    stats['inserted'] += 1
                    stats[record[-1]] += 1
            except (ValueError, TypeError, sqlite3.IntegrityError):
                stats['invalid'] += 1
    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, help='Local JSONL evidence file; never automatically crawls')
    parser.add_argument('--db', required=True, help='Local SQLite database path')
    args = parser.parse_args()
    path = Path(args.input)
    with path.open(encoding='utf-8') as src:
        def records():
            for line in src:
                if line.strip():
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        yield None
        with connect_db(args.db) as db:
            stats = ingest(records(), db)
    print(json.dumps(stats, sort_keys=True))


if __name__ == '__main__':
    main()