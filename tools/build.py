#!/usr/bin/env python3
"""PipeRoll static site generator.

Reads incidents/*.md, emits site/ : index.html, pir/<id>.html, registry.json,
registry.csv. No JS frameworks, no external assets - reference-genre pages that
render identically in 2036.
"""
import csv
import json
import os
import re
import html as htmlmod

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(ROOT, "incidents")
OUT = os.path.join(ROOT, "site")

CSS = """
:root { --ink:#111; --paper:#fff; --rule:#ddd; --link:#0645ad; --dim:#555; }
@media (prefers-color-scheme: dark) {
  :root { --ink:#e4e4e4; --paper:#1a1a1c; --rule:#3a3a3e; --link:#8ab4f8; --dim:#9c9c9c; }
}
:root[data-theme="dark"] { --ink:#e4e4e4; --paper:#1a1a1c; --rule:#3a3a3e; --link:#8ab4f8; --dim:#9c9c9c; }
:root[data-theme="light"] { --ink:#111; --paper:#fff; --rule:#ddd; --link:#0645ad; --dim:#555; }
* { box-sizing: border-box; }
body { font: 17px/1.6 Georgia, 'Times New Roman', serif; color: var(--ink);
  background: var(--paper); margin: 0 auto; max-width: 56rem; padding: 2rem 1rem 4rem; }
h1 { font-size: 1.5rem; margin: 0 0 .3rem; line-height: 1.25; }
h2 { font-size: 1.15rem; margin-top: 2rem; }
.masthead { border-bottom: 1px solid var(--rule); padding-bottom: .75rem; margin-bottom: 1.25rem; }
.masthead .org { font-size: .9rem; color: var(--dim); }
.masthead .org a { color: inherit; }
table { border-collapse: collapse; width: 100%; font-size: .85rem; }
.tablewrap { overflow-x: auto; }
th, td { text-align: left; padding: .3rem .55rem; border-bottom: 1px solid var(--rule);
  vertical-align: top; font-variant-numeric: tabular-nums; }
th { font-weight: 700; }
td:first-child, .record code { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .95em; }
a { color: var(--link); }
code { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .88em; }
.record h1 { font-size: 1.25rem; }
.record ul { padding-left: 1.2rem; }
.record li { margin: .15rem 0; }
.record p, .record li { max-width: 44rem; }
.meta { color: var(--dim); font-size: .9rem; }
.stats { margin: 1rem 0 .25rem; font-size: 1rem; }
.footer { margin-top: 3rem; border-top: 1px solid var(--rule); padding-top: .75rem;
  font-size: .85rem; color: var(--dim); }
.notice { background: none; border-left: 3px solid var(--rule); padding: .1rem 0 .1rem .9rem;
  font-size: .9rem; color: var(--dim); margin: 1rem 0; }
"""

PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head><body>
<div class="masthead">
  <div class="org"><a href="{home}">PipeRoll</a> - Agent Incident Registry</div>
  <h1>{h1}</h1>
  <div class="meta">{sub}</div>
</div>
{body}
<div class="footer">PipeRoll Agent Incident Registry - records are verified individually;
retired ids are never reused. Corrections are published, not slipped.
Machine-readable: <a href="{home_prefix}registry.json">registry.json</a> -
<a href="{home_prefix}registry.csv">registry.csv</a></div>
</body></html>
"""


def parse_record(path):
    txt = open(path, encoding="utf-8").read()
    rec = {"file": os.path.basename(path)}
    m = re.match(r"# (PIR-\d{4}-\d{4}) - (.+)", txt)
    if m:
        rec["id"], rec["title"] = m.group(1), m.group(2).strip()
    for field in ["date_occurred", "root_cause", "failure_locus", "severity",
                  "exploitation_status", "direct_loss_usd", "status", "confidence",
                  "telemetry_grade", "operator_type", "blast_radius"]:
        fm = re.search(r"`" + field + r"`:\s*(.+)", txt)
        if fm:
            rec[field] = fm.group(1).strip()
    rec["markdown"] = txt
    return rec


def build():
    os.makedirs(os.path.join(OUT, "pir"), exist_ok=True)
    records = []
    for f in sorted(os.listdir(INC)):
        if re.match(r"PIR-\d{4}-\d{4}\.md$", f):
            records.append(parse_record(os.path.join(INC, f)))

    # per-record pages
    for r in records:
        body = markdown.markdown(r["markdown"], extensions=["tables"])
        page = PAGE.format(title=f"{r['id']} - PipeRoll", css=CSS, home="../index.html",
                           home_prefix="../", h1=r["id"],
                           sub=htmlmod.escape(r.get("title", "")),
                           body=f'<div class="record">{body}</div>')
        slug = r["id"].replace("PIR-", "").lower()
        with open(os.path.join(OUT, "pir", f"{slug}.html"), "w", encoding="utf-8") as fh:
            fh.write(page)
        r["url"] = f"pir/{slug}.html"

    # exports (strip markdown body)
    export = [{k: v for k, v in r.items() if k not in ("markdown", "file")} for r in records]
    with open(os.path.join(OUT, "registry.json"), "w", encoding="utf-8") as fh:
        json.dump({"registry": "PipeRoll Agent Incident Registry",
                   "generated_from": "incidents/*.md", "records": export}, fh, indent=1)
    cols = ["id", "title", "date_occurred", "root_cause", "failure_locus", "severity",
            "exploitation_status", "direct_loss_usd", "telemetry_grade", "confidence", "status"]
    with open(os.path.join(OUT, "registry.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(export)

    # index
    def count(field):
        c = {}
        for r in records:
            v = r.get(field) or "unknown"
            m = re.search(r"`([a-z0-9-]+)`", v)
            k = m.group(1) if m else v.split(" ")[0].strip("|,;()")
            c[k] = c.get(k, 0) + 1
        return sorted(c.items(), key=lambda kv: -kv[1])

    rows = "\n".join(
        f"<tr><td><a href='{r['url']}'>{r['id']}</a></td>"
        f"<td>{htmlmod.escape(r.get('title','')[:90])}</td>"
        f"<td>{htmlmod.escape((r.get('date_occurred') or '')[:24])}</td>"
        f"<td>{htmlmod.escape((r.get('root_cause') or '')[:40])}</td>"
        f"<td>{htmlmod.escape((r.get('severity') or '')[:20])}</td>"
        f"<td>{htmlmod.escape((r.get('direct_loss_usd') or '')[:28])}</td></tr>"
        for r in records)

    def statline(field, label):
        parts = " &middot; ".join(f"{k} {n}" for k, n in count(field)[:6])
        return f"<p class='meta'><strong>{label}:</strong> {parts}</p>"

    body = f"""
<p class="stats"><strong>{len(records)} verified records</strong> &middot; 2 retired ids &middot; schema v0.1</p>
<div class="notice">Every record is individually verified against primary sources before
publication; corrections are recorded in the record itself. Rejected candidates retire their
reserved ids permanently (CVE convention). This registry is young - treat aggregate statistics
as early data, not actuarial tables.</div>
{statline('root_cause', 'Root cause')}
{statline('severity', 'Severity')}
{statline('exploitation_status', 'Exploitation status')}
<div class="tablewrap">
<table>
<tr><th>id</th><th>title</th><th>occurred</th><th>root cause</th><th>severity</th><th>direct loss</th></tr>
{rows}
</table>
</div>
"""
    page = PAGE.format(title="PipeRoll - Agent Incident Registry", css=CSS,
                       home="index.html", home_prefix="",
                       h1="Agent Incident Registry",
                       sub="Verified public records of AI-agent failures - schema, statistics, permalinks",
                       body=body)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"built {len(records)} records -> site/")


if __name__ == "__main__":
    build()
