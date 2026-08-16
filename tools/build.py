#!/usr/bin/env python3
"""PipeRoll static site generator.

Reads incidents/*.md, emits docs/ (GitHub Pages) : index.html, pir/<id>.html, registry.json,
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
OUT = os.path.join(ROOT, "docs")  # GitHub Pages serves /docs

CSS = """
/* White theme, deliberately single-theme: the registry renders on white for every viewer. */
:root, :root[data-theme="dark"], :root[data-theme="light"] {
  --ink:#111; --paper:#fff; --rule:#ddd; --link:#0645ad; --dim:#555;
  color-scheme: light;
}
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
td:nth-child(2), .record code { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .95em; }
.ord { color: var(--dim); font-size: .8em; text-align: right; }
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
.controls { display: flex; flex-wrap: wrap; gap: .5rem 1rem; align-items: center;
  margin: 1.25rem 0 .75rem; font-size: .85rem; }
.controls label { color: var(--dim); }
.controls input, .controls select, .controls button {
  font: inherit; font-size: .85rem; color: var(--ink); background: var(--paper);
  border: 1px solid var(--rule); padding: .2rem .4rem; }
.controls input { width: 14rem; max-width: 60vw; }
.grouphead { padding-top: .9rem; font-family: Georgia, serif; }
.copycite { font: inherit; font-size: .8rem; color: var(--ink); background: var(--paper);
  border: 1px solid var(--rule); padding: .05rem .5rem; margin-left: .5rem; cursor: pointer; }
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
<a href="{home_prefix}registry.csv">registry.csv</a>.
Records and data: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>
(cite PipeRoll and the PIR id). Tooling: MIT.
Archived releases: <a href="https://doi.org/10.5281/zenodo.21968992">DOI 10.5281/zenodo.21968992</a> (Zenodo, resolves to latest).</div>
</body></html>
"""


def parse_record(path):
    txt = open(path, encoding="utf-8").read()
    rec = {"file": os.path.basename(path)}
    m = re.match(r"# (PIR-\d{4}-\d{4}) - (.+)", txt)
    if m:
        rec["id"], rec["title"] = m.group(1), m.group(2).strip()
    for field in ["date_occurred", "date_disclosed", "root_cause", "failure_locus", "severity",
                  "exploitation_status", "direct_loss_usd", "status", "confidence",
                  "telemetry_grade", "operator_type", "blast_radius"]:
        fm = re.search(r"`" + field + r"`:\s*(.+)", txt)
        if fm:
            rec[field] = fm.group(1).strip()
    rec["markdown"] = txt
    return rec


def cut(s, n):
    s = (s or "").strip()
    if len(s) <= n:
        return s
    c = s[:n].rsplit(" ", 1)[0].rstrip(",;:(-")
    return c + "…"


def build():
    os.makedirs(os.path.join(OUT, "pir"), exist_ok=True)
    records = []
    for f in sorted(os.listdir(INC)):
        if re.match(r"PIR-\d{4}-\d{4}\.md$", f):
            records.append(parse_record(os.path.join(INC, f)))

    # per-record pages
    for r in records:
        body = markdown.markdown(r["markdown"], extensions=["tables"])
        occ = re.search(r"(\d{4})-(0[1-9]|1[0-2])|\b(20[12]\d)\b", r.get("date_occurred") or "")
        vintage = (f"{occ.group(1)}-{occ.group(2)}" if occ and occ.group(1)
                   else occ.group(3) if occ else "date in record")
        slug = r["id"].replace("PIR-", "").lower()
        cite_text = (f"PipeRoll {r['id']}, {cut(r.get('title', ''), 70)} ({vintage}) - "
                     f"https://piperoll.org/pir/{slug}")
        cite = (f"<div class='notice'>Cite as: {htmlmod.escape(cite_text)} "
                f"<button class='copycite' data-cite=\"{htmlmod.escape(cite_text)}\">copy</button></div>"
                "<script>document.querySelector('.copycite').addEventListener('click',function(){"
                "var b=this;navigator.clipboard.writeText(b.dataset.cite).then(function(){"
                "b.textContent='copied';setTimeout(function(){b.textContent='copy';},1500);});});</script>")
        # directory-style permalink: /pir/<slug>/ works extensionless on GitHub Pages
        page = PAGE.format(title=f"{r['id']} - PipeRoll", css=CSS, home="../../index.html",
                           home_prefix="../../", h1=r["id"],
                           sub=htmlmod.escape(r.get("title", "")),
                           body=f'{cite}<div class="record">{body}</div>')
        os.makedirs(os.path.join(OUT, "pir", slug), exist_ok=True)
        with open(os.path.join(OUT, "pir", slug, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(page)
        r["url"] = f"pir/{slug}/"

    # normalized taxonomy keys (drive filters, grouping, and export columns)
    def norm(r, field):
        v = (r.get(field) or "unknown").strip()
        m = re.match(r"^`?([a-z0-9][a-z0-9-]+)`?", v)  # v0.2: primary token leads the value
        if m:
            return m.group(1)
        m = re.search(r"`([a-z0-9-]+)`", v)
        return m.group(1) if m else v.split(" ")[0].strip("|,;()").lower() or "unknown"

    for r in records:
        r["cause_key"] = norm(r, "root_cause")
        r["severity_key"] = norm(r, "severity")
        r["status_key"] = norm(r, "exploitation_status")
        r["locus_key"] = norm(r, "failure_locus")
        # best available chronology: occurrence date, else disclosure date (research demos).
        # month/day validated - naive \d{2} reads "2022-2023" as month 20.
        sd = None
        for fld in ("date_occurred", "date_disclosed"):
            v = r.get(fld) or ""
            m = re.search(r"(\d{4})-(0[1-9]|1[0-2])(?:-(0[1-9]|[12]\d|3[01]))?", v)
            if m:
                sd = f"{m.group(1)}-{m.group(2)}-{m.group(3) or '00'}"
                break
            y = re.search(r"\b(20[12]\d)\b", v)
            if y:
                sd = f"{y.group(1)}-00-00"
                break
        r["sort_date"] = sd or "0000-00-00"
        r["year_key"] = r["sort_date"][:4] if sd else "n/a"

    # exports (strip markdown body)
    export = [{k: v for k, v in r.items() if k not in ("markdown", "file")} for r in records]
    with open(os.path.join(OUT, "registry.json"), "w", encoding="utf-8") as fh:
        json.dump({"registry": "PipeRoll Agent Incident Registry",
                   "generated_from": "incidents/*.md", "records": export}, fh, indent=1)
    cols = ["id", "title", "date_occurred", "cause_key", "locus_key", "severity_key",
            "status_key", "year_key", "root_cause", "failure_locus", "severity",
            "exploitation_status", "direct_loss_usd", "telemetry_grade", "confidence", "status"]
    with open(os.path.join(OUT, "registry.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(export)

    # index
    def count(key):
        c = {}
        for r in records:
            c[r[key]] = c.get(r[key], 0) + 1
        return sorted(c.items(), key=lambda kv: -kv[1])

    def options(key, label):
        opts = "".join(f"<option value='{k}'>{k} ({n})</option>" for k, n in count(key))
        return (f"<label>{label} <select data-filter='{key}'>"
                f"<option value=''>all</option>{opts}</select></label>")

    def date_cell(r):
        if r["sort_date"] == "0000-00-00":
            return "n/a"
        d = r["sort_date"]
        while d.endswith("-00"):
            d = d[:-3]
        occ = r.get("date_occurred") or ""
        if not re.search(r"(\d{4})-(0[1-9]|1[0-2])|\b20[12]\d\b", occ):
            return f"{d} (disclosed)"
        return d

    def loss_cell(r):
        v = (r.get("direct_loss_usd") or "").strip()
        return cut(v.split("(")[0].strip() or v, 26)

    display = sorted(records, key=lambda r: (r["sort_date"], r["id"]), reverse=True)
    rows = "\n".join(
        f"<tr data-cause_key='{r['cause_key']}' data-severity_key='{r['severity_key']}'"
        f" data-status_key='{r['status_key']}' data-locus_key='{r['locus_key']}'"
        f" data-year_key='{r['year_key']}' data-sortdate='{r['sort_date']}' data-id='{r['id']}'"
        f" data-text='{htmlmod.escape((r['id'] + ' ' + r.get('title','') + ' ' + r['cause_key'] + ' ' + r['status_key']).lower())}'>"
        f"<td class='ord'>{i + 1}</td>"
        f"<td><a href='{r['url']}'>{r['id']}</a></td>"
        f"<td>{htmlmod.escape(cut(r.get('title',''), 90))}</td>"
        f"<td>{htmlmod.escape(date_cell(r))}</td>"
        f"<td>{htmlmod.escape(r['cause_key'])}</td>"
        f"<td>{htmlmod.escape(r['severity_key'])}</td>"
        f"<td>{htmlmod.escape(loss_cell(r))}</td></tr>"
        for i, r in enumerate(display))

    controls = f"""
<div class="controls">
  <label>search <input type="search" id="q" autocomplete="off" placeholder="id, title, cause&hellip;"></label>
  {options('cause_key', 'root cause')}
  {options('severity_key', 'severity')}
  {options('status_key', 'exploitation')}
  {options('locus_key', 'locus')}
  <label>sort <select id="sortby">
    <option value="newest">newest first</option><option value="oldest">oldest first</option>
    <option value="registration">id order</option></select></label>
  <label>group by <select id="groupby">
    <option value="">none</option><option value="cause_key">root cause</option>
    <option value="severity_key">severity</option><option value="year_key">year</option>
    <option value="status_key">exploitation</option></select></label>
  <button id="reset" type="button">reset</button>
  <span class="meta" id="shown"></span>
</div>"""

    script = """
<script>
(function () {
  var tbody = document.querySelector('#registry tbody');
  var all = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
  var selects = document.querySelectorAll('select[data-filter]');
  var q = document.getElementById('q'), groupby = document.getElementById('groupby');
  var sortby = document.getElementById('sortby');
  var shown = document.getElementById('shown');
  // browsers restore form state across soft reloads; a reference page must never open pre-filtered
  q.value = ''; groupby.value = ''; sortby.value = 'newest';
  selects.forEach(function (s) { s.value = ''; });
  function cmp(a, b, key, dir) {
    return a.dataset[key] < b.dataset[key] ? -dir : a.dataset[key] > b.dataset[key] ? dir : 0;
  }
  function apply() {
    var text = q.value.toLowerCase().trim();
    var active = [];
    selects.forEach(function (s) { if (s.value) active.push([s.dataset.filter, s.value]); });
    var kept = all.filter(function (tr) {
      if (text && tr.dataset.text.indexOf(text) === -1) return false;
      return active.every(function (f) { return tr.dataset[f[0]] === f[1]; });
    });
    var mode = sortby.value;
    if (mode === 'registration') kept.sort(function (a, b) { return cmp(a, b, 'id', 1); });
    else kept.sort(function (a, b) { return cmp(a, b, 'sortdate', mode === 'oldest' ? 1 : -1); });
    tbody.innerHTML = '';
    var g = groupby.value;
    if (!g) { kept.forEach(function (tr) { tbody.appendChild(tr); }); }
    else {
      var groups = {};
      kept.forEach(function (tr) { (groups[tr.dataset[g]] = groups[tr.dataset[g]] || []).push(tr); });
      Object.keys(groups).sort(function (a, b) { return groups[b].length - groups[a].length; })
        .forEach(function (k) {
          var h = document.createElement('tr');
          h.innerHTML = "<th colspan='7' class='grouphead'>" + k + ' (' + groups[k].length + ')</th>';
          tbody.appendChild(h);
          groups[k].forEach(function (tr) { tbody.appendChild(tr); });
        });
    }
    kept.forEach(function (tr, i) {
      var ord = tr.querySelector('.ord');
      if (ord) ord.textContent = i + 1;
    });
    shown.textContent = kept.length + ' of ' + all.length + ' records';
  }
  selects.forEach(function (s) { s.addEventListener('change', apply); });
  q.addEventListener('input', apply);
  groupby.addEventListener('change', apply);
  sortby.addEventListener('change', apply);
  document.getElementById('reset').addEventListener('click', function () {
    q.value = ''; groupby.value = ''; sortby.value = 'newest';
    selects.forEach(function (s) { s.value = ''; });
    apply();
  });
  apply();
})();
</script>"""

    def statline(key, label):
        parts = " &middot; ".join(f"{k} {n}" for k, n in count(key)[:6])
        return f"<p class='meta'><strong>{label}:</strong> {parts}</p>"

    body = f"""
<p class="stats"><strong>{len(records)} verified records</strong> &middot; 0 retired ids &middot; schema v0.2</p>
<div class="notice">Every record is individually verified against primary sources before
publication; corrections are recorded in the record itself. Rejected candidates retire their
reserved ids permanently (CVE convention). Id numbering: the initial import (0001-0045,
registered Aug 2026) is ordered by occurrence date, oldest first, as a one-time property;
from here on ids are assigned at registration, so sequence is not guaranteed chronological
for later records. The year in the id is the registration year. This registry is young -
treat aggregate statistics as early data, not actuarial tables.
<br><br>Completeness: this registry records publicly reported, verifiable incidents - a fraction
of what occurs. Most agent failures are never disclosed, and coverage skews toward incidents
that are visible (on-chain losses, court records, published research) and English-language
sources. Counts here are a floor, never an estimate of true frequency; the absence of a
system from this registry is not evidence of its safety, and no failure rate can be computed
from registry counts alone because the exposure base (how many agents run, doing what) is
unknown.</div>
{statline('cause_key', 'Root cause')}
{statline('severity_key', 'Severity')}
{statline('status_key', 'Exploitation status')}
{controls}
<div class="tablewrap">
<table id="registry">
<thead><tr><th>#</th><th>id</th><th>title</th><th>occurred</th><th>root cause</th><th>severity</th><th>direct loss</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
{script}
"""
    page = PAGE.format(title="PipeRoll - Agent Incident Registry", css=CSS,
                       home="index.html", home_prefix="",
                       h1="Agent Incident Registry",
                       sub="Verified public records of AI-agent failures - schema, statistics, permalinks",
                       body=body)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page)

    # deployment furniture (GitHub Pages)
    with open(os.path.join(OUT, "CNAME"), "w") as fh:
        fh.write("piperoll.org\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write("User-agent: *\nAllow: /\nSitemap: https://piperoll.org/sitemap.xml\n")
    urls = ["https://piperoll.org/"] + [f"https://piperoll.org/{r['url']}" for r in records]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    notfound = PAGE.format(title="Not found - PipeRoll", css=CSS, home="/index.html",
                           home_prefix="/", h1="404 - no such record",
                           sub="The id you followed does not exist in this registry.",
                           body="<p>If a citation led you here, the id may be mistyped - "
                                "check the <a href='/index.html'>registry index</a>. "
                                "PipeRoll ids are never deleted or reused, so a once-valid "
                                "permalink stays valid.</p>")
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(notfound)
    print(f"built {len(records)} records -> docs/")


if __name__ == "__main__":
    build()
