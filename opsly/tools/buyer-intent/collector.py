#!/usr/bin/env python3
"""Opt-in, allowlisted HTTPS RSS collector. Dry-run unless --execute is supplied.

No automatic discovery, secret, authentication, redirect, or third-party posting.
"""
import argparse
import ipaddress
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

MAX_FEEDS = 10
MAX_BYTES = 2_000_000
LABEL = re.compile(r'^[a-z0-9][a-z0-9_-]{0,79}$')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('feed redirects are not approved')


def validate_feed(feed):
    """Require a recorded source label and exactly authorized DNS hostname."""
    if not isinstance(feed, dict) or set(feed) != {'label', 'url', 'approved_host'}:
        raise ValueError('source must contain only label, url and approved_host')
    label, url, approved = feed['label'], feed['url'], feed['approved_host']
    if any(not isinstance(x, str) for x in (label, url, approved)) or not LABEL.fullmatch(label):
        raise ValueError('invalid source label or URL fields')
    parts = urlsplit(url)
    hostname = (parts.hostname or '').lower()
    if (parts.scheme != 'https' or not hostname or hostname != approved.lower() or
            parts.username or parts.password or parts.fragment or parts.port not in (None, 443)):
        raise ValueError('URL is not an approved HTTPS RSS endpoint')
    if hostname == 'localhost' or hostname.endswith('.local') or '.' not in hostname:
        raise ValueError('private hostname is not allowed')
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        raise ValueError('IP-literal feed URLs are not allowed')
    return feed


def load_sources(path):
    feeds = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(feeds, list) or len(feeds) > MAX_FEEDS:
        raise ValueError('sources must be a JSON list of up to 10 entries')
    labels = set()
    for feed in feeds:
        validate_feed(feed)
        if feed['label'] in labels:
            raise ValueError('duplicate source label')
        labels.add(feed['label'])
    return feeds


def retrieve(feed, opener=None):
    validate_feed(feed)
    opener = opener or urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(feed['url'],
        headers={'User-Agent': 'OpslySwarm/0.1 (permitted public RSS reader)', 'Accept': 'application/rss+xml, application/atom+xml, text/xml, application/xml'},
        method='GET')
    with opener.open(req, timeout=12) as response:
        if response.geturl() != feed['url']:
            raise ValueError('feed redirected from its approved URL')
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('feed exceeds maximum allowed bytes')
    if not raw.lstrip().startswith(b'<'):
        raise ValueError('source is not XML')
    return raw


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sources', required=True, help='Operator-approved public RSS source manifest')
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--execute', action='store_true', help='Network access; opt-in only')
    args = ap.parse_args()
    feeds = load_sources(args.sources)
    if not args.execute:
        print(json.dumps({'mode': 'dry-run', 'configured_sources': [f['label'] for f in feeds]}))
        return
    directory = Path(args.out_dir)
    directory.mkdir(parents=True, exist_ok=True)
    saved, failed = [], []
    for feed in feeds:
        try:
            raw = retrieve(feed)
            path = directory / (feed['label'] + '.xml')
            temporary = directory / (feed['label'] + '.tmp')
            temporary.write_bytes(raw)
            os.replace(temporary, path)
            saved.append(feed['label'])
        except (OSError, ValueError, urllib.error.URLError):
            failed.append(feed['label'])
    print(json.dumps({'mode': 'execute', 'saved': saved, 'failed': failed}))
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()