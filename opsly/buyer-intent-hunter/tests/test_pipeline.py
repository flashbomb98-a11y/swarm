"""No-network unit tests for zero-cost evidence intake and deduplication."""
import importlib.util
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / 'pipeline.py'
spec = importlib.util.spec_from_file_location('opsly_pipeline', FILE)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
NOW = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)


def candidate(**changes):
    data = {'candidate_id': 'abc-1', 'source_url': 'https://community.example.com/t/123?utm_source=ads',
            'request_text': 'Looking for a freelancer to build a website. Budget 500 EUR. Urgent.',
            'discovered_at': NOW.isoformat(), 'source_label': 'permitted-feed'}
    data.update(changes)
    return data


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute('''CREATE TABLE candidates (candidate_id TEXT PRIMARY KEY, source_url TEXT UNIQUE,
            request_text TEXT, discovered_at TEXT, source_label TEXT, text_hash TEXT UNIQUE,
            score INTEGER, bucket TEXT, evidence_status TEXT DEFAULT 'unverified',
            outreach_status TEXT DEFAULT 'not_sent')''')

    def tearDown(self):
        self.db.close()

    def test_positive_request_review(self):
        self.assertEqual(p.ingest([candidate()], self.db, NOW)['review'], 1)
        score, bucket, evidence, outreach = self.db.execute(
            'SELECT score,bucket,evidence_status,outreach_status FROM candidates').fetchone()
        self.assertGreaterEqual(score, 45)
        self.assertEqual((bucket, evidence, outreach), ('review', 'unverified', 'not_sent'))

    def test_duplicate_tracking_and_mirror(self):
        a = candidate()
        b = candidate(candidate_id='abc-2', source_url='https://community.example.com/t/123')
        c = candidate(candidate_id='abc-3', source_url='https://other.example.com/new')
        self.assertEqual(p.ingest([a,b,c], self.db, NOW)['duplicates'], 2)

    def test_marketing_excluded(self):
        stats = p.ingest([candidate(request_text='We offer cheap web design today!')], self.db, NOW)
        self.assertEqual(stats['reject_promotion'], 1)

    def test_weak_request_watch(self):
        self.assertEqual(p.ingest([candidate(request_text='Is this a good software stack?')], self.db, NOW)['watch'], 1)

    def test_stale_does_not_qualify(self):
        self.assertEqual(p.ingest([candidate(discovered_at=(NOW-timedelta(days=45)).isoformat())], self.db, NOW)['stale'], 1)

    def test_future_or_naive_date_rejected(self):
        records = [candidate(discovered_at=(NOW+timedelta(days=1)).isoformat()), candidate(candidate_id='x', discovered_at='2026-10-09T12:00:00')]
        self.assertEqual(p.ingest(records, self.db, NOW)['invalid'], 2)

    def test_insecure_and_private_sources_rejected(self):
        bad = ['http://example.com/t/1', 'https://localhost/t/1', 'https://127.0.0.1/t/1', 'https://user:pass@example.com/', 'https://10.0.0.4/x']
        for url in bad:
            with self.subTest(url=url):
                self.assertEqual(p.ingest([candidate(source_url=url)], self.db, NOW)['invalid'], 1)

    def test_missing_fields_rejected(self):
        self.assertEqual(p.ingest([{'candidate_id': 'a'}], self.db, NOW)['invalid'], 1)

    def test_no_fabricated_review_or_outreach(self):
        p.ingest([candidate()], self.db, NOW)
        row = self.db.execute('SELECT evidence_status,outreach_status FROM candidates').fetchone()
        self.assertEqual(row, ('unverified', 'not_sent'))

    def test_german_intent(self):
        stats = p.ingest([candidate(request_text='Suche Unterstützung bei Wordpress, Budget 200 EUR')], self.db, NOW)
        self.assertEqual(stats['review'], 1)

    def test_cli_persists_across_imports(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, db = Path(tmp)/'items.jsonl', Path(tmp)/'items.sqlite'
            source.write_text(json.dumps(candidate(discovered_at='2026-10-08T12:00:00+00:00'))+'\n', encoding='utf-8')
            first = subprocess.run([sys.executable,str(FILE),'--input',str(source),'--db',str(db)],capture_output=True,text=True,check=True)
            second = subprocess.run([sys.executable,str(FILE),'--input',str(source),'--db',str(db)],capture_output=True,text=True,check=True)
            self.assertEqual(json.loads(first.stdout)['inserted'], 1)
            self.assertEqual(json.loads(second.stdout)['duplicates'], 1)


if __name__ == '__main__':
    unittest.main()