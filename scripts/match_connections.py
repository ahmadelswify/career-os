#!/usr/bin/env python3
"""Find referral paths in your own LinkedIn connections. Standard library only (Python 3.9+).

Input is the Connections.csv LinkedIn lets you download (Settings > Data privacy >
Get a copy of your data > Connections). Nothing is fetched from LinkedIn.

The Company column is whatever the person last wrote on their profile, so it can be
stale. Old connections are flagged, and loose name matches ("Northwind" vs "Northwind Pet
Supply") are marked partial so you confirm the company before asking anyone.

Usage:
  python3 scripts/match_connections.py Connections.csv [--targets "Northwind,Acme"]
         [--watchlist Companies/watchlist.json] [--role "product,analytics"] [--json]
Targets come from --targets, else from the watchlist (name plus optional "aliases").
"""
import csv
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

SUFFIXES = {"inc", "llc", "ltd", "corp", "corporation", "co", "company", "the", "plc", "gmbh", "sa", "ag", "holdings", "group"}
RECRUITER = re.compile(r"recruit|talent|sourc|people partner|hr business", re.I)
SENIOR = re.compile(r"\b(head|director|vp|vice president|chief|lead|principal|senior manager|manager)\b", re.I)
STALE_AFTER_DAYS = 2 * 365


def normalize(name):
    words = re.sub(r"[^a-z0-9 ]+", " ", (name or "").lower()).split()
    return " ".join(w for w in words if w not in SUFFIXES)


def read_connections(path):
    lines = Path(path).read_text(encoding="utf-8-sig", errors="replace").splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("First Name")), 0)
    return list(csv.DictReader(lines[start:]))


def parse_connected(value):
    for fmt in ("%d %b %Y", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime((value or "").strip(), fmt).date()
        except ValueError:
            pass
    return None


def match_kind(company, target):
    c = normalize(company)
    names = [normalize(target["name"])] + [normalize(a) for a in target.get("aliases", [])]
    if c in names:
        return "exact"
    for n in names:
        if n and (set(n.split()) <= set(c.split()) or set(c.split()) <= set(n.split())) and c:
            return "partial"
    return None


def match(rows, targets, role_keywords=(), today=None):
    today = date.fromisoformat(today) if today else date.today()
    kw = [k.lower() for k in role_keywords if k]
    out = {}
    for t in targets:
        found = []
        for r in rows:
            kind = match_kind(r.get("Company", ""), t)
            if not kind:
                continue
            pos = r.get("Position", "") or ""
            why, score = [], 0
            if kind == "exact":
                score += 100
            if kw and any(k in pos.lower() for k in kw):
                why.append("same function as the role")
                score += 30
            if RECRUITER.search(pos):
                why.append("recruiter, can route your resume")
                score += 20
            if SENIOR.search(pos):
                why.append("senior, may know the hiring manager")
                score += 10
            connected = parse_connected(r.get("Connected On"))
            stale = bool(connected and (today - connected).days > STALE_AFTER_DAYS)
            checks = []
            if kind == "partial":
                checks.append(f"Confirm it's the same company: their profile says \"{r.get('Company')}\".")
            if stale:
                checks.append("Connected over 2 years ago; their company may have changed.")
            found.append({
                "name": f"{r.get('First Name', '').strip()} {r.get('Last Name', '').strip()}".strip(),
                "position": pos,
                "company_on_profile": r.get("Company", ""),
                "url": r.get("URL", ""),
                "connected_on": r.get("Connected On", ""),
                "match": kind,
                "stale": stale,
                "why": "; ".join(why) or "works there",
                "check": " ".join(checks),
                "_score": score - (15 if stale else 0),
            })
        found.sort(key=lambda x: (-x["_score"], x["name"]))
        for f in found:
            del f["_score"]
        out[t["name"]] = found
    return out


def main(argv):
    def opt(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default

    files = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or not argv[i - 1].startswith("--"))]
    if not files:
        print(__doc__)
        return 2
    if opt("--targets"):
        targets = [{"name": n.strip()} for n in opt("--targets").split(",") if n.strip()]
    else:
        wl = Path(opt("--watchlist", "Companies/watchlist.json"))
        targets = [{"name": c["name"], "aliases": c.get("aliases", [])} for c in json.loads(wl.read_text()).get("companies", [])] if wl.exists() else []
    if not targets:
        print("No target companies. Pass --targets or add companies to the watchlist.")
        return 2
    result = match(read_connections(files[0]), targets, (opt("--role", "") or "").split(","))
    if "--json" in argv:
        print(json.dumps(result, indent=2))
        return 0
    for company, people in result.items():
        print(f"\n{company}: {len(people)} connection(s)")
        for p in people:
            print(f"  - {p['name']}, {p['position']} ({p['match']}): {p['why']}" + (f"  [check: {p['check']}]" if p["check"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
