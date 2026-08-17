#!/usr/bin/env python3
"""Submit every source URL in incidents/*.md to the Internet Archive's
Wayback Machine (Save Page Now).

Why: a registry claim is only as durable as the page it cites. Archiving at
registration freezes what the source said, with the Internet Archive's own
timestamps as the independent witness - the forensic question a dispute asks
is "what did the source say then", not "does the link still resolve".

Run from a machine with open egress (the build sandbox blocks arbitrary HTTP):
    python3 tools/archive.py                     # all records
    python3 tools/archive.py PIR-2026-0047       # one or more records
    python3 tools/archive.py --dry-run           # list URLs, no network
    python3 tools/archive.py --force             # archive even if fresh

A URL with an existing snapshot younger than --max-age-days (default 180) is
skipped to respect Save Page Now rate limits. Anonymous submission works;
set IA_ACCESS_KEY / IA_SECRET (archive.org S3-style keys) for the
authenticated endpoint and friendlier limits.

Exit code is 0 unless --strict is given and any submission failed: Wayback
outages must not masquerade as registry regressions.
"""
import argparse
import glob
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linkcheck import urls_of  # single source of truth for URL extraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(ROOT, "incidents")
UA = {"User-Agent": "Mozilla/5.0 (PipeRoll source-archiver; +https://piperoll.org)"}
AVAILABILITY = "https://archive.org/wayback/available?url={}"
SPN_ANON = "https://web.archive.org/save/{}"
SPN_AUTH = "https://web.archive.org/save"


def record_files(names):
    if not names:
        return sorted(glob.glob(os.path.join(INC, "PIR-*.md")))
    out = []
    for n in names:
        n = n if n.endswith(".md") else n + ".md"
        path = os.path.join(INC, os.path.basename(n))
        if not os.path.exists(path):
            sys.exit(f"no such record: {n}")
        out.append(path)
    return out


def collect(files):
    """unique URL -> [record ids], preserving first-seen order."""
    seen = {}
    for f in files:
        rid = os.path.basename(f)[:-3]
        for url, _known_debt in urls_of(f):
            seen.setdefault(url, []).append(rid)
    return seen


def latest_snapshot(url):
    """(timestamp 'YYYYMMDDhhmmss' or None) via the availability API."""
    try:
        req = urllib.request.Request(
            AVAILABILITY.format(urllib.parse.quote(url, safe="")), headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        snap = (data.get("archived_snapshots") or {}).get("closest") or {}
        if snap.get("available"):
            return snap.get("timestamp")
    except Exception:
        pass
    return None


def age_days(timestamp):
    try:
        then = time.mktime(time.strptime(timestamp[:8], "%Y%m%d"))
        return (time.time() - then) / 86400
    except Exception:
        return None


def save(url):
    """Submit one URL to Save Page Now. Returns (ok, detail)."""
    key, secret = os.environ.get("IA_ACCESS_KEY", ""), os.environ.get("IA_SECRET", "")
    try:
        if key and secret:
            body = urllib.parse.urlencode({"url": url}).encode()
            req = urllib.request.Request(SPN_AUTH, data=body, method="POST",
                                         headers={**UA,
                                                  "Accept": "application/json",
                                                  "Authorization": f"LOW {key}:{secret}"})
        else:
            req = urllib.request.Request(SPN_ANON.format(url), headers=UA)
        with urllib.request.urlopen(req, timeout=120) as r:
            return True, f"HTTP {r.status}"
    except Exception as e:
        return False, str(e)[:120]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Archive record sources to the Wayback Machine.")
    ap.add_argument("records", nargs="*", help="record ids (default: all)")
    ap.add_argument("--dry-run", action="store_true", help="list URLs, no network")
    ap.add_argument("--force", action="store_true", help="submit even if a fresh snapshot exists")
    ap.add_argument("--max-age-days", type=int, default=180,
                    help="existing snapshot younger than this is fresh enough")
    ap.add_argument("--delay", type=float, default=15,
                    help="seconds between submissions (Save Page Now is rate-limited)")
    ap.add_argument("--strict", action="store_true", help="nonzero exit on any failure")
    args = ap.parse_args(argv)

    targets = collect(record_files(args.records))
    print(f"{len(targets)} unique source URLs "
          f"across {len(record_files(args.records))} record(s)")
    if args.dry_run:
        for url, rids in targets.items():
            print(f"  {url}  [{', '.join(rids)}]")
        return 0

    saved = skipped = failed = 0
    for i, (url, rids) in enumerate(targets.items()):
        if not args.force:
            ts = latest_snapshot(url)
            age = age_days(ts) if ts else None
            if age is not None and age <= args.max_age_days:
                print(f"SKIP  {url}  (snapshot {ts[:8]}, {age:.0f}d old)")
                skipped += 1
                continue
        ok, detail = save(url)
        if ok:
            print(f"SAVED {url}  ({detail})")
            saved += 1
        else:
            print(f"FAIL  {url}  ({detail})  [{', '.join(rids)}]")
            failed += 1
        if i < len(targets) - 1:
            time.sleep(args.delay)

    print(f"\nsaved {saved}, skipped {skipped} (fresh), failed {failed}")
    return 1 if (args.strict and failed) else 0


if __name__ == "__main__":
    sys.exit(main())
