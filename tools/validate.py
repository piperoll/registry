#!/usr/bin/env python3
"""Schema validator for PIR records - the deterministic gate on every PR.

Usage:
    python3 tools/validate.py                 # validate all records
    python3 tools/validate.py incidents/PIR-2026-0045.md ...   # validate specific files

Errors fail the run (exit 1); warnings do not. Enum lists mirror
incident-schema-v0.md v0.2 - change them together.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(ROOT, "incidents")

ENUMS = {
    "root_cause": {"prompt-injection", "memory-poisoning", "credential-exposure",
                   "model-update-regression", "tool-error", "policy-violation",
                   "plain-error", "operator-error", "adversarial-other",
                   "supply-chain-compromise"},
    "severity": {"near-miss", "degraded", "loss", "catastrophic"},
    "exploitation_status": {"in-wild-exploited", "in-wild-malfunction",
                            "in-wild-payload-failed", "researcher-demonstrated",
                            "bounty-game", "unknown"},
    "failure_locus": {"agent-reasoning", "harness", "tool-mcp", "dependency",
                      "model-provider", "operator-config", "unknown"},
}
REQUIRED = ["id", "title", "date_occurred", "root_cause", "severity",
            "exploitation_status", "failure_locus", "mechanism", "sources", "confidence"]
DATE_OK = re.compile(r"(\d{4})-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?|\b20[12]\d\b|n/a|not applicable")
ID_RX = re.compile(r"^PIR-\d{4}-\d{4}$")


def field(txt, name):
    m = re.search(r"`" + name + r"`:\s*(.+?)(?=\n- `|\n#|\n\n|\Z)", txt, re.S)
    return m.group(1).strip() if m else None


def check(path):
    errors, warnings = [], []
    fname = os.path.basename(path)
    txt = open(path, encoding="utf-8").read()

    m = re.match(r"# (PIR-\d{4}-\d{4}) - (.+)", txt)
    if not m:
        errors.append("first line must be '# PIR-YYYY-NNNN - <title>'")
    head_id = m.group(1) if m else None

    fid = field(txt, "id")
    if not fid or not ID_RX.match(fid):
        errors.append(f"id field missing or malformed: {fid!r}")
    else:
        if fid != fname[:-3]:
            errors.append(f"id {fid} != filename {fname}")
        if head_id and fid != head_id:
            errors.append(f"id field {fid} != heading id {head_id}")

    for name in REQUIRED:
        if name in ("id", "title"):
            continue
        if field(txt, name) is None:
            errors.append(f"required field missing: {name}")

    for name, allowed in ENUMS.items():
        v = field(txt, name)
        if v is None:
            continue
        tok = re.match(r"`?([a-z0-9][a-z0-9-]+)`?", v)
        tok = tok.group(1) if tok else ""
        if tok not in allowed:
            errors.append(f"{name}: primary token {tok!r} not in enum {sorted(allowed)}")

    # only occurrence demands chronology; detection/disclosure are often honestly
    # relative ("immediate", "same session") and time_to_detect carries the number
    v = field(txt, "date_occurred")
    if v and not (DATE_OK.search(v) or re.search(r"\b20[12]\ds\b|unknown", v)):
        errors.append(f"date_occurred: no parseable date/year/decade and not n-a/unknown: {v[:60]!r}")

    src = field(txt, "sources") or ""
    urls = re.findall(r"https://[^\s;,)\]>'\"]+", src)
    if not urls:
        errors.append("sources: no https:// URL found")
    unverified = src.count("unverified:")
    if unverified:
        warnings.append(f"sources: {unverified} entry(ies) labeled unverified (known debt)")

    tg = field(txt, "telemetry_grade") or ""
    if tg and not re.match(r"`?(none|operator-logs|append-only|witnessed)\b", tg):
        warnings.append(f"telemetry_grade should lead with none|operator-logs|append-only|witnessed: {tg[:40]!r}")

    ap = field(txt, "adversary_present") or ""
    if ap and not re.match(r"(yes|no|unknown)\b", ap):
        warnings.append(f"adversary_present should be yes|no|unknown: {ap[:40]!r}")

    return errors, warnings


def main():
    paths = sys.argv[1:] or [os.path.join(INC, f) for f in sorted(os.listdir(INC))
                             if re.match(r"PIR-\d{4}-\d{4}\.md$", f)]
    total_e = total_w = 0
    ids = set()
    for p in paths:
        errors, warnings = check(p)
        fid = os.path.basename(p)[:-3]
        if fid in ids:
            errors.append("duplicate id")
        ids.add(fid)
        for e in errors:
            print(f"ERROR {os.path.basename(p)}: {e}")
        for w in warnings:
            print(f"warn  {os.path.basename(p)}: {w}")
        total_e += len(errors)
        total_w += len(warnings)
    print(f"\n{len(paths)} records checked: {total_e} errors, {total_w} warnings")
    sys.exit(1 if total_e else 0)


if __name__ == "__main__":
    main()
