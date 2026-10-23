#!/usr/bin/env python3
"""Watch companies for changes. Standard library only (Python 3.9+).

Reads Companies/watchlist.json, fetches each public source, compares it with the
last snapshot in .watch/, and prints only what changed: new or closed roles,
new or updated site pages, changed page text, new repo activity.

Read-only by design: public GETs, robots.txt respected for websites, no logins.

Source types:
  greenhouse  {"board": "<board token>"}   public job board API
  lever       {"company": "<slug>"}         public postings API
  ashby       {"org": "<slug>"}             public job board API
  sitemap     {"url": "https://.../sitemap.xml"}
  page        {"url": "https://..."}        any page; reports added/removed lines of text
  github      {"org": "<org>"}              public repos and when they were last pushed

Usage:
  python3 scripts/watch.py [--json] [--dry-run] [--watchlist PATH] [--snapshots DIR]
The first run for a source records a snapshot and reports nothing for it.
"""
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

USER_AGENT = "career-os-watch/1.0 (+https://github.com/ahmadelswify/career-os)"
SITE_TYPES = ("sitemap", "page")
MAX_PAGE_LINES = 400


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def source_url(src):
    t = src["type"]
    if t == "greenhouse":
        return f"https://boards-api.greenhouse.io/v1/boards/{src['board']}/jobs"
    if t == "lever":
        return f"https://api.lever.co/v0/postings/{src['company']}?mode=json"
    if t == "ashby":
        return f"https://api.ashbyhq.com/posting-api/job-board/{src['org']}"
    if t == "github":
        return f"https://api.github.com/orgs/{src['org']}/repos?sort=pushed&per_page=50"
    if t in SITE_TYPES:
        return src["url"]
    raise ValueError(f"unknown source type: {t}")


def source_label(src):
    t = src["type"]
    ident = src.get("board") or src.get("company") or src.get("org") or src.get("url")
    return f"{t} {ident}"


def job(title, location, url):
    return " · ".join(x for x in (title, location, url) if x)


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "tr", "section", "br", "a"):
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def parse(kind, raw):
    """Turn a fetched body into {key: summary} so snapshots diff cleanly."""
    if kind == "greenhouse":
        return {str(j["id"]): job(j.get("title"), (j.get("location") or {}).get("name"), j.get("absolute_url"))
                for j in json.loads(raw).get("jobs", [])}
    if kind == "lever":
        return {str(j["id"]): job(j.get("text"), (j.get("categories") or {}).get("location"), j.get("hostedUrl"))
                for j in json.loads(raw)}
    if kind == "ashby":
        return {j.get("jobUrl") or j.get("id"): job(j.get("title"), j.get("location"), j.get("jobUrl"))
                for j in json.loads(raw).get("jobs", [])}
    if kind == "github":
        return {r["name"]: f"pushed {(r.get('pushed_at') or '')[:10]}" for r in json.loads(raw)}
    if kind == "sitemap":
        root = ET.fromstring(raw)
        out = {}
        for el in root.iter():
            if el.tag.endswith("}url") or el.tag == "url" or el.tag.endswith("}sitemap") or el.tag == "sitemap":
                loc = next((c.text for c in el if c.tag.endswith("loc")), None)
                mod = next((c.text for c in el if c.tag.endswith("lastmod")), "") or ""
                if loc:
                    out[loc.strip()] = mod.strip()
        return out
    if kind == "page":
        p = _Text()
        p.feed(raw.decode("utf-8", errors="replace"))
        lines = []
        for line in "".join(p.parts).splitlines():
            line = re.sub(r"\s+", " ", line).strip()
            if line and line not in lines:
                lines.append(line)
        return {line: "" for line in lines[:MAX_PAGE_LINES]}
    raise ValueError(f"unknown source type: {kind}")


def diff(old, new, page=False):
    out = []
    for k in new:
        if k not in old:
            out.append({"kind": "added", "key": k, "detail": k if page else new[k]})
    for k in old:
        if k not in new:
            out.append({"kind": "removed", "key": k, "detail": k if page else old[k]})
    if not page:
        for k in new:
            if k in old and old[k] != new[k]:
                out.append({"kind": "changed", "key": k, "detail": f"{old[k]} -> {new[k]}"})
    return out


def allowed(url, fetch, cache):
    parts = urlparse(url)
    base = f"{parts.scheme}://{parts.netloc}"
    if base not in cache:
        rp = RobotFileParser()
        try:
            rp.parse(fetch(base + "/robots.txt").decode("utf-8", errors="replace").splitlines())
        except Exception:
            rp.parse([])  # no robots.txt: allowed
        cache[base] = rp
    return cache[base].can_fetch(USER_AGENT, url)


def run(watchlist, snapshot_dir, fetch=http_get, dry_run=False):
    snapshot_dir = Path(snapshot_dir)
    result = {"changes": [], "seeded": [], "errors": [], "skipped": []}
    robots = {}
    for co in watchlist.get("companies", []):
        name = co["name"]
        slug = co.get("slug") or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        snap_file = snapshot_dir / f"{slug}.json"
        snap = json.loads(snap_file.read_text()) if snap_file.exists() else {}
        for src in co.get("sources", []):
            label = source_label(src)
            try:
                url = source_url(src)
                if src["type"] in SITE_TYPES and not allowed(url, fetch, robots):
                    result["skipped"].append(f"{name}: {label} (robots.txt disallows it)")
                    continue
                current = parse(src["type"], fetch(url))
            except urllib.error.HTTPError as e:  # report and keep the old snapshot
                why = "not found (check the board or org name)" if e.code == 404 else f"HTTP {e.code}"
                result["errors"].append(f"{name}: {label}: {why}")
                continue
            except Exception as e:  # report and keep the old snapshot
                result["errors"].append(f"{name}: {label}: {e}")
                continue
            if label not in snap:
                result["seeded"].append(f"{name}: {label}")
            else:
                for ch in diff(snap[label], current, page=src["type"] == "page"):
                    result["changes"].append({"company": name, "source": label, **ch})
            snap[label] = current
        if not dry_run:
            snapshot_dir.mkdir(parents=True, exist_ok=True)
            snap_file.write_text(json.dumps(snap, indent=1, sort_keys=True))
    return result


def summary(result):
    lines = [f"[{c['company']}] {c['source']}: {c['kind']} {c['detail']}" for c in result["changes"]]
    if result["seeded"]:
        lines.insert(0, f"First snapshot recorded for {len(result['seeded'])} source(s); changes show from the next run.")
    if not lines:
        lines.append("No changes since the last run.")
    lines += [f"Skipped: {s}" for s in result["skipped"]]
    lines += [f"Error: {e}" for e in result["errors"]]
    return lines


def main(argv):
    def opt(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    watchlist_path = Path(opt("--watchlist", "Companies/watchlist.json"))
    if not watchlist_path.exists():
        print(f"No watchlist at {watchlist_path}. Copy templates/watchlist.json there and add companies.")
        return 2
    result = run(json.loads(watchlist_path.read_text()), Path(opt("--snapshots", ".watch")), dry_run="--dry-run" in argv)
    if "--json" in argv:
        print(json.dumps(result, indent=2))
        return 0
    print("\n".join(summary(result)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
