#!/usr/bin/env python3
"""Offline zero-dependency QA for the portable Opsly static storefront."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

HTML = Path(__file__).with_name("index.html")
BRANDS = ("Opsly Sales", "Opsly Web Studio", "Opsly Business",
          "Opsly Tools", "Opsly Visual", "Opsly Audio", "Opsly Lab")
SECRET_PATTERNS = (r"sk_(?:live|test)_[A-Za-z0-9]+", r"whsec_[A-Za-z0-9]+",
                   r"rk_(?:live|test)_[A-Za-z0-9]+")

class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.errors = []
        self.scripts = 0
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if "id" in attr:
            if attr["id"] in self.ids:
                self.errors.append("duplicate id: " + attr["id"])
            self.ids.add(attr["id"])
        if tag == "a":
            self.links.append(attr.get("href", ""))
        if tag == "script":
            self.scripts += 1

def main():
    content = HTML.read_text(encoding="utf-8")
    parser = Links()
    parser.feed(content)
    errors = list(parser.errors)
    if not content.lower().lstrip().startswith("<!doctype html>"):
        errors.append("missing HTML5 DOCTYPE")
    for brand in BRANDS:
        if brand not in content:
            errors.append("missing business line: " + brand)
    for href in parser.links:
        if not href:
            errors.append("anchor without href")
        elif href.startswith("#") and href[1:] not in parser.ids:
            errors.append("broken local anchor: " + href)
        elif not (href.startswith("#") or href.startswith("mailto:") or
                  (urlparse(href).scheme == "https" and urlparse(href).netloc)):
            errors.append("unsupported or insecure link: " + href)
    if not any(x.startswith("mailto:opsly-sales@agentmail.to") for x in parser.links):
        errors.append("no customer service contact")
    if not any(x.startswith("https://opsly-market.floot.app/") for x in parser.links):
        errors.append("no current commercial checkout destination")
    if parser.scripts:
        errors.append("standby site unexpectedly includes script tags")
    if not re.search(r'<meta name="robots" content="noindex,nofollow"', content):
        errors.append("standby page has no noindex until independent deploy")
    for rule in SECRET_PATTERNS:
        if re.search(rule, content):
            errors.append("hardcoded credential/token")
    if "noch keinen eigenständigen Checkout" not in content:
        errors.append("standby site must disclose checkout limitation")
    # Shared Opsly design tokens must stay identical across releases.
    palette = ("#111821", "#25303C", "#1B262E", "#3C4A54", "#C8FF3D", "#F6F8F7", "#B9C6CA")
    for hex_color in palette:
        if hex_color not in content:
            errors.append("canonical palette color missing: " + hex_color)
    for typo in ("OpslyCo", "OplsyCo", "Opslyshop", "OpslyShop"):
        if typo in content:
            errors.append("forbidden public brand alias: " + typo)
    unknown_colors = set(re.findall(r"#[0-9a-fA-F]{6}\\b", content)) - set(palette)
    if unknown_colors:
        errors.append("non-brand CSS colors: " + ", ".join(sorted(unknown_colors)))
    if errors:
        print("FAILED:\n - " + "\n - ".join(errors))
        return 1
    print(f"PASSED: {len(BRANDS)} Opsly lanes; {len(parser.links)} links; "
          f"{len(parser.ids)} IDs; no private keys/scripts; email intake present.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
