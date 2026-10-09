"""No-network compliance-focused collector tests."""
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

FILE = Path(__file__).resolve().parents[1] / 'collector.py'
spec = importlib.util.spec_from_file_location('collector', FILE)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def feed(**updates):
    x={'label':'approved-feed','url':'https://example.org/rss.xml','approved_host':'example.org'}
    x.update(updates)
    return x


class CollectorTest(unittest.TestCase):
    def test_feed_host_validation(self):
        self.assertEqual(collector.validate_feed(feed())['label'],'approved-feed')

    def test_rejects_mismatched_domain(self):
        with self.assertRaises(ValueError):
            collector.validate_feed(feed(url='https://evil.org/rss.xml'))

    def test_rejects_unsafe_urls(self):
        urls = ['http://example.org/rss.xml','https://localhost/rss','https://127.0.0.1/rss',
                'https://user:pw@example.org/rss.xml','https://example.org:8443/rss']
        for url in urls:
            with self.subTest(url=url), self.assertRaises(ValueError):
                collector.validate_feed(feed(url=url,approved_host=(__import__('urllib.parse', fromlist=['urlsplit']).urlsplit(url).hostname or '')))

    def test_registry_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'feeds.json'
            source.write_text(json.dumps([feed(),feed()]))
            with self.assertRaises(ValueError): collector.load_sources(source)

    def test_empty_registry_has_no_network(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'feeds.json'
            source.write_text('[]')
            self.assertEqual(collector.load_sources(source),[])

    def test_download_has_size_limit(self):
        class MockResponse:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def geturl(self): return 'https://example.org/rss.xml'
            def read(self, n): return b'<' + b'x'*collector.MAX_BYTES
        class Opener:
            def open(self,*args,**kwargs): return MockResponse()
        with self.assertRaises(ValueError): collector.retrieve(feed(), opener=Opener())

    def test_redirect_to_unapproved_url_rejected(self):
        class Redirected:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def geturl(self): return 'https://malicious.example/feed'
        class Opener:
            def open(self,*args,**kwargs): return Redirected()
        with self.assertRaises(ValueError): collector.retrieve(feed(),opener=Opener())


if __name__ == '__main__': unittest.main()