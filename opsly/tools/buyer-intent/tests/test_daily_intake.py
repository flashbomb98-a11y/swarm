"""No-network regression tests for daily buyer-intent report."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import daily_intake


class DailyDigestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.config = self.path / 'approved.json'
        self.config.write_text(json.dumps([{
            'label': 'hn-freelance',
            'url': 'https://hnrss.org/whoishiring/freelance',
            'approved_host': 'hnrss.org',
        }]), encoding='utf-8')
        self.db = self.path / 'evidence.sqlite'
        self.out = self.path / 'sanitized-report.json'
        self.now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
        self.feed = b'''<rss><channel>
          <item><title>Looking for a freelance Python developer with budget $2000</title>
            <link>https://news.ycombinator.com/item?id=100</link>
            <pubDate>Fri, 09 Oct 2026 11:00:00 GMT</pubDate>
          </item>
          <item><title>We offer promo code for hosting</title>
            <link>https://news.ycombinator.com/item?id=101</link>
            <pubDate>Fri, 09 Oct 2026 11:00:00 GMT</pubDate>
          </item>
        </channel></rss>'''

    def test_dry_run_never_touches_network_or_db(self):
        def forbidden(_):
            raise AssertionError('network called')
        output = daily_intake.run(self.config, self.db, self.out,
                                  fetcher=forbidden, now=self.now)
        self.assertEqual(output['mode'], 'dry-run')
        self.assertFalse(self.db.exists())
        self.assertFalse(self.out.exists())

    def test_review_report_contains_only_links_and_metadata(self):
        daily_intake.run(self.config, self.db, self.out, execute=True,
                         fetcher=lambda _: self.feed, now=self.now)
        report = json.loads(self.out.read_text(encoding='utf-8'))
        self.assertEqual(report['new_review_candidates'], 1)
        self.assertEqual(report['outreach_sent'], 0)
        self.assertEqual(report['leads'][0]['status'], 'UNVERIFIED - manual review required')
        self.assertNotIn('freelance Python developer', self.out.read_text())
        self.assertNotIn('promo code', self.out.read_text())

    def test_repeat_deduplicates_existing_candidates(self):
        for _ in range(2):
            daily_intake.run(self.config, self.db, self.out, execute=True,
                             fetcher=lambda _: self.feed, now=self.now)
        self.assertEqual(json.loads(self.out.read_text())['new_review_candidates'], 0)

    def test_job_seeker_post_is_not_sold_as_a_customer_lead(self):
        self.feed = b'''<rss><channel>
          <item><title>SEEKING WORK | Looking for website projects with budget</title>
            <link>https://news.ycombinator.com/item?id=201</link>
            <pubDate>Fri, 09 Oct 2026 11:00:00 GMT</pubDate></item>
          <item><title>SEEKING FREELANCER | Need a landing page. Budget $600</title>
            <link>https://news.ycombinator.com/item?id=202</link>
            <pubDate>Fri, 09 Oct 2026 11:00:00 GMT</pubDate></item>
        </channel></rss>'''
        daily_intake.run(self.config, self.db, self.out, execute=True,
                         fetcher=lambda _: self.feed, now=self.now)
        report = json.loads(self.out.read_text(encoding='utf-8'))
        self.assertEqual(report['statistics']['reject_supplier'], 1)
        self.assertEqual(report['new_review_candidates'], 1)
        self.assertEqual(report['leads'][0]['source_url'],
                         'https://news.ycombinator.com/item?id=202')

    def test_source_error_fails_closed(self):
        def broken(_):
            raise ValueError('invalid feed')
        with self.assertRaises(RuntimeError):
            daily_intake.run(self.config, self.db, self.out, execute=True,
                             fetcher=broken, now=self.now)
        self.assertFalse(self.out.exists())

    def test_empty_source_list_refuses_execution(self):
        self.config.write_text('[]')
        with self.assertRaises(ValueError):
            daily_intake.run(self.config, self.db, self.out, execute=True,
                             fetcher=lambda _: self.feed, now=self.now)


if __name__ == '__main__':
    unittest.main()
