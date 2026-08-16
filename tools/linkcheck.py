#!/usr/bin/env python3
"""Fetch-grade liveness check for every source URL in incidents/*.md.

Run from a machine with open egress (the build sandbox blocks arbitrary HTTP):
    python3 tools/linkcheck.py            # check all
    python3 tools/linkcheck.py PIR-2026-0013   # check one record

Prints one line per URL: status code or error. Exit code 1 if any URL fails.
URLs already labeled "unverified:" in a record are reported but do not fail
the run - they are known debts, not regressions.
"""
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(ROOT, "incidents")
UA = {"User-Agent": "Mozilla/5.0 (PipeRoll linkcheck; +https://piperoll.org)"}


def urls_of(path):
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"`sources`:\s*(.+?)(?:\n- `|\n#|\Z)", txt, re.S)
    if not m:
        return []
    src = m.group(1)
    out = []
    # commas are legal inside URLs (Mata_v._Avianca,_Inc.) - split on whitespace
    # and angle quotes only, then strip trailing sentence punctuation
    for u in re.findall(r"https?://[^\s<>\"']+", src):
        u = u.rstrip(".;,)]")
        known_debt = f"unverified: {u}" in src or f"unverified:{u}" in src
        out.append((u, known_debt))
    return out


GUARDED = {401, 403, 405, 406, 429, 999}  # alive but hostile to robots


def check(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status
        except Exception as e:  # try GET after HEAD failure; report last error
            err = e
    return err


def classify(res):
    """ok | guarded | slow | FAIL - only proof-of-death fails the run.

    Bot-blockers answer a robot differently than a reader; a link check must
    not fail on 403/429-class hostility or slow hosts. Hard failure means the
    URL provably has no document: 404/410, DNS failure, connection refused.
    """
    import socket
    import urllib.error
    if isinstance(res, urllib.error.HTTPError):
        res = res.code
    if isinstance(res, int):
        if res < 400:
            return "ok"
        if res in (404, 410):
            return "FAIL"
        return "guarded"
    if isinstance(res, socket.timeout) or "timed out" in str(res):
        return "slow"
    return "FAIL"


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    failed = 0
    total = 0
    for f in sorted(os.listdir(INC)):
        if not re.match(r"PIR-\d{4}-\d{4}\.md$", f):
            continue
        if only and not f.startswith(only):
            continue
        for url, known_debt in urls_of(os.path.join(INC, f)):
            total += 1
            res = check(url)
            tag = classify(res)
            if known_debt and tag == "FAIL":
                tag = "known-debt"
            if tag == "FAIL":
                failed += 1
            print(f"{tag:10} {res!s:>26.26}  {f[:16]}  {url}")
    print(f"\n{total} urls checked, {failed} failures")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
