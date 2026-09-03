#!/usr/bin/env python3
"""PipeRoll incident-discovery pipeline (v0).

Gathers candidate leads from configured sources, scores them against the
registry's scope, dedupes against the published registry and a running seen-list,
and writes the survivors to candidates/<date>.md for EDITORIAL triage.

It never writes a record and never opens a PR against incidents/. Discovery feeds
verification; it does not replace it (constitution: every record is individually
verified against primary sources before entry).

    python3 discovery/discover.py            # run with discovery/config.json
    python3 discovery/discover.py --dry-run  # print, do not write files
"""
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sources  # noqa: E402
import triage  # noqa: E402

CONFIG = os.path.join(HERE, "config.json")
REGISTRY_JSON = os.path.join(ROOT, "docs", "registry.json")
CAND_DIR = os.path.join(ROOT, "candidates")
SEEN = os.path.join(CAND_DIR, "seen.txt")
INTAKE = ("https://github.com/piperoll/registry/issues/new?"
          "template=incident-report.yml")


def load_seen():
    if not os.path.exists(SEEN):
        return set()
    return {ln.strip() for ln in open(SEEN, encoding="utf-8") if ln.strip()}


def render(cands, date):
    lines = [
        f"# Candidate leads - {date}", "",
        "> **Unverified leads, not registry records.** These are machine-surfaced",
        "> pointers for editorial review; none carries a PIR id, and nothing here is",
        "> published to piperoll.org. A lead becomes a record only after a human",
        "> verifies it against primary sources and it passes the scope test",
        "> (\"the subject is always an agent\"). Reject freely; false positives are",
        "> expected while the filter is tuned.", "",
        f"{len(cands)} lead(s) this run. To register one, open the "
        f"[incident intake form]({INTAKE}).", "",
    ]
    for c in cands:
        lines += [
            f"## {c.get('title','(untitled)')}",
            f"- source: {c.get('source','?')}"
            + (f" &middot; {c['date']}" if c.get("date") else "")
            + (f" &middot; {c['cve']}" if c.get("cve") else ""),
            f"- url: {c.get('url','')}",
            f"- score: {c.get('_score')} ({'; '.join(c.get('_reasons', []))})",
            f"- why look: {(c.get('summary') or '').strip()[:280]}",
            "",
        ]
    return "\n".join(lines) + "\n"


def main():
    dry = "--dry-run" in sys.argv
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"discovery run {date} (dry-run={dry})")

    raw = sources.gather(cfg)
    print(f"gathered {len(raw)} raw items")
    seen = load_seen()
    cands = triage.triage(raw, cfg, REGISTRY_JSON, seen)
    print(f"{len(cands)} candidate(s) after scope + dedup (min_score={cfg.get('min_score')})")

    if dry:
        for c in cands:
            print(f"  [{c['_score']}] {c.get('title','')[:80]}  <{c.get('url','')}>")
        return

    if not cands:
        print("no new candidates - nothing written")
        return

    os.makedirs(CAND_DIR, exist_ok=True)
    out = os.path.join(CAND_DIR, f"{date}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(cands, date))
    # remember what we proposed so we don't re-surface it tomorrow
    with open(SEEN, "a", encoding="utf-8") as f:
        for c in cands:
            u = triage._norm_url(c.get("url"))
            if u:
                f.write(u + "\n")
    print(f"wrote {out} ({len(cands)} candidates); updated {os.path.basename(SEEN)}")


if __name__ == "__main__":
    main()
