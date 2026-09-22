#!/usr/bin/env python3
"""
1688 Product Data Fetcher

Fetches a 1688 product page and extracts structured data from embedded JSON and meta tags.
No paid API required. Uses curl and HTML/JSON parsing.

Usage:
    python3 fetch_1688_data.py <1688-url> [--output <path>]

Output: JSON to stdout (and optionally to file)
"""

import argparse
import json
import re
import subprocess
import sys
from typing import Optional
from html.parser import HTMLParser
from urllib.parse import urlparse


def extract_offer_id(url: str) -> Optional[str]:
    """Extract offerId from various 1688 URL patterns."""
    patterns = [
        r"offer/(\d+)",
        r"offerId=(\d+)",
        r"/(\d{10,})\.html",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def fetch_page(url: str) -> str:
    """Fetch page HTML with curl, clearing proxy vars."""
    cmd = [
        "/bin/zsh", "-lc",
        f'HTTP_PROXY="" HTTPS_PROXY="" http_proxy="" https_proxy="" '
        f'curl -sL --max-time 30 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        f'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" '
        f'"{url}"',
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        return result.stdout
    except Exception as e:
        return f""


class MetaTagParser(HTMLParser):
    """Extract meta tags and title from HTML."""

    def __init__(self):
        super().__init__()
        self.meta = {}
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "meta":
            key = attrs_d.get("property") or attrs_d.get("name") or ""
            val = attrs_d.get("content", "")
            if key and val:
                self.meta[key] = val
        elif tag == "title":
            self._in_title = True

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def extract_meta(html: str) -> dict:
    """Extract og:title, og:image, og:description and page title."""
    parser = MetaTagParser()
    try:
        parser.feed(html)
    except Exception:
        pass
    return {
        "title": parser.title or parser.meta.get("og:title", ""),
        "image": parser.meta.get("og:image", ""),
        "description": parser.meta.get("og:description", parser.meta.get("description", "")),
        "keywords": parser.meta.get("keywords", ""),
    }


def extract_embedded_json(html: str) -> dict:
    """Try to find embedded JSON data blocks in the page."""
    result = {}

    # Strategy 1: window.__data = {...};
    for pattern in [
        r"window\.__data\s*=\s*(\{.*?\})\s*;",
        r"window\.TB\s*=\s*(\{.*?\})\s*;",
        r"window\._dida_config\s*=\s*(\{.*?\})\s*;",
        r"window\.runParams\s*=\s*(\{.*?\})\s*;",
    ]:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                result["embedded_json"] = data
                break
            except json.JSONDecodeError:
                continue

    # Strategy 2: <script type="application/json" id="...">{...}</script>
    for match in re.finditer(
        r'<script[^>]*type=["\']application/json["\'][^>]*>(\{.*?\})</script>',
        html, re.DOTALL,
    ):
        try:
            data = json.loads(match.group(1))
            if "embedded_scripts" not in result:
                result["embedded_scripts"] = []
            result["embedded_scripts"].append(data)
        except json.JSONDecodeError:
            continue

    # Strategy 3: Look for specific data fields
    # title
    title_match = re.search(r'"subject"\s*:\s*"([^"]+)"', html)
    if title_match:
        result["subject"] = title_match.group(1)

    # sellingPoints
    sp_match = re.search(r'"sellingPoints"\s*:\s*\[(.*?)\]', html, re.DOTALL)
    if sp_match:
        try:
            sp_raw = "[" + sp_match.group(1) + "]"
            result["sellingPoints"] = json.loads(sp_raw)
        except (json.JSONDecodeError, IndexError):
            # Try extracting individual strings
            points = re.findall(r'"([^"]+)"', sp_match.group(1))
            if points:
                result["sellingPoints"] = points

    # productAttributes
    pa_match = re.search(r'"productAttributes"\s*:\s*(\[.*?\])', html, re.DOTALL)
    if pa_match:
        try:
            result["productAttributes"] = json.loads(pa_match.group(1))
        except json.JSONDecodeError:
            pass

    # price
    price_match = re.search(r'"price"\s*:\s*"?([\d.]+)"?', html)
    if price_match:
        result["price"] = price_match.group(1)

    # minOrderQuantity
    moq_match = re.search(r'"minOrderQuantity"\s*:\s*(\d+)', html)
    if moq_match:
        result["minOrderQuantity"] = int(moq_match.group(1))

    # productImage images
    img_match = re.search(r'"images"\s*:\s*\[(.*?)\]', html, re.DOTALL)
    if img_match:
        urls = re.findall(r'"(https?://[^"]+)"', img_match.group(1))
        if urls:
            result["images"] = urls

    # companyName
    company_match = re.search(r'"companyName"\s*:\s*"([^"]+)"', html)
    if company_match:
        result["companyName"] = company_match.group(1)

    return result


def extract_text_fallbacks(html: str) -> dict:
    """Extract text-based fallbacks when JSON parsing fails."""
    result = {}

    # Remove script and style tags
    clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    clean = re.sub(r"<style[^>]*>.*?</style>", "", clean, flags=re.DOTALL)
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    if clean:
        result["page_text"] = clean[:5000]

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch and parse 1688 product page")
    parser.add_argument("url", help="1688 product URL")
    parser.add_argument("--output", "-o", help="Output file path", default=None)
    args = parser.parse_args()

    offer_id = extract_offer_id(args.url)
    if not offer_id:
        print(json.dumps({"error": f"Could not extract offerId from URL: {args.url}"}, ensure_ascii=False))
        sys.exit(1)

    html = fetch_page(args.url)
    if not html or len(html) < 500:
        print(json.dumps({
            "error": "Failed to fetch page or page too short. The page may be JS-rendered.",
            "offerId": offer_id,
            "url": args.url,
            "hint": "Use the in-app browser to load the URL and extract content manually.",
        }, ensure_ascii=False))
        sys.exit(1)

    meta = extract_meta(html)
    embedded = extract_embedded_json(html)
    fallbacks = extract_text_fallbacks(html)

    output = {
        "offerId": offer_id,
        "url": args.url,
        "meta": meta,
        "embedded": embedded,
        "fallbacks": fallbacks,
        "fetch_status": "success" if meta.get("title") or embedded.get("subject") else "partial",
    }

    # Clean up empty values
    if not embedded:
        del output["embedded"]
    if not fallbacks:
        del output["fallbacks"]

    json_output = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"Saved to {args.output}", file=sys.stderr)

    print(json_output)


if __name__ == "__main__":
    main()
