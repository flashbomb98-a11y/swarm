"""Local RSS and Atom tests; no HTTP requests."""
import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / 'rss_adapter.py'
spec = importlib.util.spec_from_file_location('rss_adapter', FILE)
rss = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rss)


class FeedTests(unittest.TestCase):
    def test_rss_candidate(self):
        xml = b'''<rss><channel><item><title>Looking for developer</title>
        <link>https://example.net/job/2</link>
        <pubDate>Thu, 08 Oct 2026 10:00:00 GMT</pubDate>
        </item></channel></rss>'''
        records = rss.candidates(xml, 'test-feed')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['source_label'], 'test-feed')
        self.assertEqual(records[0]['discovered_at'], '2026-10-08T10:00:00+00:00')

    def test_rss_description_is_used_for_buyer_intent(self):
        xml = b'''<rss><channel><item><title>Discussion thread</title>
        <description><![CDATA[<p>Looking for a freelance developer with budget</p>]]></description>
        <link>https://example.net/job/32</link>
        <pubDate>Fri, 09 Oct 2026 11:00:00 GMT</pubDate>
        </item></channel></rss>'''
        records = rss.candidates(xml, 'test-feed')
        self.assertEqual(len(records), 1)
        self.assertIn('Looking for a freelance developer', records[0]['request_text'])
        self.assertNotIn('<p>', records[0]['request_text'])

    def test_atom_candidate(self):
        xml = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
        <title>Suche Webdesign</title><link rel="alternate" href="https://example.net/a/1"/>
        <updated>2026-10-08T12:00:00Z</updated></entry></feed>'''
        records = rss.candidates(xml, 'atom-feed')
        self.assertEqual(records[0]['source_url'], 'https://example.net/a/1')

    def test_skip_missing_date(self):
        xml = b'<rss><channel><item><title>hello</title><link>https://example.net/j</link></item></channel></rss>'
        self.assertEqual(rss.candidates(xml, 'x'), [])

    def test_dtd_rejected(self):
        with self.assertRaises(ValueError):
            rss.candidates(b'<!DOCTYPE rss><rss/>', 'x')

    def test_max_bytes(self):
        with self.assertRaises(ValueError):
            rss.candidates(b'x' * (rss.MAX_BYTES+1), 'x')

    def test_deterministic_candidate_identity(self):
        xml = b'''<rss><item><title>Suche</title><link>https://example.net/q</link>
        <pubDate>Thu, 08 Oct 2026 10:00:00 GMT</pubDate></item></rss>'''
        first = rss.candidates(xml, 'a')[0]['candidate_id']
        second = rss.candidates(xml, 'b')[0]['candidate_id']
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()