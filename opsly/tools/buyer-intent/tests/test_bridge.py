"""No-network tests for the opt-in authenticated Division event gateway."""
import importlib.util
import io
import json
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bridge', ROOT / 'bridge.py')
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def test_payload_exact_and_idempotent(self):
        row = ('cand-11', 'https://example.org/r/1', 'Looking for help', '2026-10-09T10:00:00Z', 'feed')
        result = bridge.publication(row, 'bundle-v2:sha256:' + 'a'*64)
        self.assertEqual(result['method'], 'event.publish')
        self.assertEqual(result['params']['event_name'], 'intent.candidate.received')
        self.assertEqual(result['params']['idempotency_key'], 'opsly-intake:cand-11')
        self.assertEqual(result['params']['payload']['source_url'], row[1])

    def test_hash_is_required(self):
        with self.assertRaises(ValueError):
            bridge.publication(('x','a','b','c','d'), 'invalid')

    def test_publish_requires_https(self):
        with self.assertRaises(ValueError):
            bridge.publish('http://example.com', 'secret', {})

    def test_dry_run_has_no_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp)/'c.sqlite')
            with sqlite3.connect(db_path) as db:
                db.execute('CREATE TABLE candidates (candidate_id TEXT PRIMARY KEY, source_url TEXT,request_text TEXT, discovered_at TEXT, source_label TEXT,bucket TEXT)')
                db.execute("INSERT INTO candidates VALUES ('xx','https://example.com/r','Looking for help','2026-10-09T10:00:00Z','feed','review')")
            with patch('sys.argv', ['bridge.py','--db',db_path]), patch.object(bridge, 'publish', side_effect=AssertionError('network attempted')):
                buf=io.StringIO()
                with redirect_stdout(buf): bridge.main()
                self.assertEqual(json.loads(buf.getvalue())['would_publish'], 1)


if __name__ == '__main__':
    unittest.main()