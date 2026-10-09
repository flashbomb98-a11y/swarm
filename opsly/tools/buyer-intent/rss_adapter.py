#!/usr/bin/env python3
"""Convert permitted, locally supplied RSS/Atom XML into auditable candidate JSONL.

This adapter never connects to the internet. Collection/permission is a distinct step.
"""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlsplit

MAX_BYTES = 2_000_000
MAX_ITEMS = 100


def parsedate(value):
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
    except (ValueError, TypeError, IndexError):
        try:
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return None
    if not dt.tzinfo or not dt.utcoffset() and dt.tzinfo is None:
        return None
    return dt.astimezone(timezone.utc).isoformat()


def _child_text(node, local_name):
    for child in node:
        if child.tag.rsplit('}', 1)[-1] == local_name:
            return (child.text or '').strip()
    return ''


def candidates(xml_bytes, source_label):
    if len(xml_bytes) > MAX_BYTES:
        raise ValueError('feed exceeds size limit')
    head = xml_bytes[:500].upper()
    if b'<!DOCTYPE' in xml_bytes.upper() or b'<!ENTITY' in xml_bytes.upper():
        raise ValueError('DTD/entities not allowed in feed')
    root = ET.fromstring(xml_bytes)
    results = []
    for entry in root.iter():
        tag = entry.tag.rsplit('}', 1)[-1]
        if tag not in ('item', 'entry'):
            continue
        link = _child_text(entry, 'link')
        if tag == 'entry':
            for child in entry:
                if child.tag.rsplit('}', 1)[-1] == 'link' and child.attrib.get('rel', 'alternate') == 'alternate':
                    link = child.attrib.get('href', link)
                    break
        stamp = _child_text(entry, 'pubDate') or _child_text(entry, 'published') or _child_text(entry, 'updated')
        date = parsedate(stamp)
        text = _child_text(entry, 'title') or _child_text(entry, 'summary') or _child_text(entry, 'description')
        if not (urlsplit(link).scheme == 'https' and date and text):
            continue
        identity = hashlib.sha256(link.encode('utf-8')).hexdigest()[:24]
        results.append({'candidate_id': identity, 'source_url': link,
                        'request_text': text[:10000], 'discovered_at': date,
                        'source_label': source_label})
        if len(results) >= MAX_ITEMS:
            break
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--xml-file', required=True, help='Permitted RSS/Atom feed saved locally')
    ap.add_argument('--source-label', required=True)
    ap.add_argument('--output', required=True, help='Local JSONL file')
    a = ap.parse_args()
    contents = Path(a.xml_file).read_bytes()
    records = candidates(contents, a.source_label)
    with Path(a.output).open('w', encoding='utf-8') as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False)+'\n')
    print(json.dumps({'converted': len(records)}))


if __name__ == '__main__':
    main()