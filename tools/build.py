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
import subprocess
import html as htmlmod

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(ROOT, "incidents")
OUT = os.path.join(ROOT, "docs")  # GitHub Pages serves /docs

CSS = """
/* White theme, deliberately single-theme: the registry renders on white for every viewer. */
:root, :root[data-theme="dark"], :root[data-theme="light"] {
  --ink:#111; --paper:#fff; --rule:#ddd; --link:#0645ad; --dim:#555;
  --key:#0f6674; --chip:#f4f4f1;
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
.footer p { margin: .25rem 0; }
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
/* record page: section heads and field keys scan differently from values */
.record h3 { font-size: .95rem; color: var(--dim); text-transform: uppercase;
  letter-spacing: .06em; border-bottom: 1px solid var(--rule); padding-bottom: .15rem;
  margin: 1.5rem 0 .5rem; }
.record code { color: var(--key); background: var(--chip); padding: 0 .25em;
  border-radius: 2px; }
.record a, .notice, .record code { overflow-wrap: anywhere; }
/* small screens */
@media (max-width: 640px) {
  body { padding: 1rem .75rem 3rem; font-size: 16px; }
  h1 { font-size: 1.25rem; }
  .controls { gap: .4rem .6rem; font-size: .8rem; }
  .controls input { width: 100%; max-width: 100%; }
  .controls label { flex: 1 1 45%; }
  table { font-size: .78rem; }
  th, td { padding: .25rem .4rem; }
  .record p, .record li { max-width: 100%; }
}
"""

PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head><body>
<div class="masthead">
  <div class="org"><a href="{home}">PipeRoll</a> - Agent Incident Registry &middot;
    <a href="{home_prefix}about/">about</a> &middot;
    <a href="{home_prefix}contribute/">contribute</a> &middot;
    <a href="{home_prefix}data/">data</a></div>
  <h1>{h1}</h1>
  <div class="meta">{sub}</div>
</div>
{body}
<div class="footer">
<p>PipeRoll Agent Incident Registry - records are verified individually; retired ids are
never reused; corrections are published, not slipped.</p>
<p><a href="{home_prefix}about/">About</a> &middot;
<a href="{home_prefix}contribute/">Contribute</a> &middot;
<a href="{home_prefix}data/">Data &amp; formats</a> &middot;
records <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, tooling MIT &middot;
archived releases <a href="https://doi.org/10.5281/zenodo.21968992">DOI 10.5281/zenodo.21968992</a>.{footer_extra}</p>
</div>
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


def registered_info(relpath):
    """(author, date) of the commit that added this record path, from git."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%an|%as", "--", relpath],
            cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip()
        if out:
            name, date = out.splitlines()[-1].split("|", 1)
            return name.strip(), date.strip()
    except Exception:
        pass
    return None, None


def linkify(html_body):
    """Turn bare https URLs in rendered record HTML into anchors.

    Guarded against touching attribute values (preceded by quote or =) and
    keeps trailing punctuation outside the link.
    """
    def repl(m):
        url, tail = m.group(1), m.group(2)
        return f'<a href="{url}">{url}</a>{tail}'
    return re.sub(r'(?<!["\'=])(https://[^\s<>"\']+?)([.,;)\]]*)(?=[\s<]|$)',
                  repl, html_body)


def build():
    os.makedirs(os.path.join(OUT, "pir"), exist_ok=True)
    records = []
    for f in sorted(os.listdir(INC)):
        if re.match(r"PIR-\d{4}-\d{4}\.md$", f):
            records.append(parse_record(os.path.join(INC, f)))

    # per-record pages
    for r in records:
        body = markdown.markdown(r["markdown"], extensions=["tables"], tab_length=2)
        occ = re.search(r"(\d{4})-(0[1-9]|1[0-2])|\b(20[12]\d)\b", r.get("date_occurred") or "")
        vintage = (f"{occ.group(1)}-{occ.group(2)}" if occ and occ.group(1)
                   else occ.group(3) if occ else "date in record")
        slug = r["id"].replace("PIR-", "").lower()
        permalink = f"https://piperoll.org/pir/{slug}"
        cite_text = f"PipeRoll {r['id']}, {cut(r.get('title', ''), 70)} ({vintage}) - {permalink}"
        cite_html = (f"PipeRoll {r['id']}, {htmlmod.escape(cut(r.get('title', ''), 70))} ({vintage}) - "
                     f"<a href=\"{permalink}\">{permalink}</a>")
        bib = ("@misc{" + r['id'].replace('-', '_') + ",\n"
               "  title = {" + r.get('title', '') + "},\n"
               "  howpublished = {\\url{" + permalink + "}},\n"
               "  year = {" + (vintage[:4] if vintage[:4].isdigit() else "n.d.") + "},\n"
               "  note = {PipeRoll Agent Incident Registry, " + r['id'] +
               ". Registry DOI: 10.5281/zenodo.21968992}\n}")
        reg_name, reg_date = registered_info(f"incidents/{r['id']}.md")
        reg_line = (f" Registered {reg_date} by {htmlmod.escape(reg_name)}." if reg_name else "")
        cite = (f"<div class='notice'>Cite as: {cite_html} "
                f"<button class='copycite' data-cite=\"{htmlmod.escape(cite_text)}\">copy</button> "
                f"<button class='copycite' data-cite=\"{htmlmod.escape(bib)}\">bibtex</button> "
                f"<a href=\"{permalink}.md\">markdown</a>.{reg_line}</div>"
                "<script>document.querySelectorAll('.copycite').forEach(function(b){"
                "b.addEventListener('click',function(){var l=b.textContent;"
                "navigator.clipboard.writeText(b.dataset.cite).then(function(){"
                "b.textContent='copied';setTimeout(function(){b.textContent=l;},1500);});});});</script>")
        # directory-style permalink: /pir/<slug>/ works extensionless on GitHub Pages
        page = PAGE.format(title=f"{r['id']} - PipeRoll", css=CSS, home="../../index.html",
                           home_prefix="../../", h1=r["id"], footer_extra="",
                           sub=htmlmod.escape(r.get("title", "")),
                           body=f'{cite}<div class="record">{linkify(body)}</div>')
        os.makedirs(os.path.join(OUT, "pir", slug), exist_ok=True)
        with open(os.path.join(OUT, "pir", slug, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(page)
        with open(os.path.join(OUT, "pir", f"{slug}.md"), "w", encoding="utf-8") as fh:
            fh.write(r["markdown"])
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
<thead><tr><th>#</th><th>id</th><th>title</th><th>occurred</th><th>root cause</th><th>severity</th><th>direct loss (USD)</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
{script}
"""
    maintainer_foot = ('\nMaintained by <a href="https://github.com/srinivasgumdelli">Srinivas Gumdelli</a> - '
                       'source and submissions at '
                       '<a href="https://github.com/piperoll/registry">github.com/piperoll/registry</a>.')
    page = PAGE.format(title="PipeRoll - Agent Incident Registry", css=CSS,
                       home="index.html", home_prefix="", footer_extra=maintainer_foot,
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
                           home_prefix="/", h1="404 - no such record", footer_extra="",
                           sub="The id you followed does not exist in this registry.",
                           body="<p>If a citation led you here, the id may be mistyped - "
                                "check the <a href='/index.html'>registry index</a>. "
                                "PipeRoll ids are never deleted or reused, so a once-valid "
                                "permalink stays valid.</p>")
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(notfound)

    # about page
    about_body = """<div class="record">
<p>PipeRoll is a public registry of verified AI-agent incidents: what the agent controlled,
what went wrong, what it cost, and what the evidence is. It is named for the Pipe Rolls -
the English Exchequer's great rolls, 676 unbroken years of audited records kept
tamper-evident by a parallel copy in different hands.</p>
<h3>Principles</h3>
<ul>
<li>Every record is verified individually against primary sources before publication.</li>
<li>Corrections are published in the record, never slipped.</li>
<li>Rejected candidates retire their reserved ids permanently; ids are never reused.</li>
<li>Ids are permanent opaque names; chronology lives in the record, vintage in the citation.</li>
<li>Near-misses are records too - full exposure with zero realized loss is actuarially precious.</li>
</ul>
<h3>Completeness</h3>
<p>The registry records publicly reported, verifiable incidents - a fraction of what occurs,
biased toward the visible (on-chain losses, court records, published research, English-language
sources). Counts are a floor, never a frequency estimate; absence from the registry is not
evidence of safety; and no failure rate can be computed from registry counts alone, because
the exposure base is unknown.</p>
<h3>Citing</h3>
<p>Each record page carries a plain citation and a BibTeX entry with copy buttons, plus a raw
markdown endpoint for machine use. Registry-level archives carry a DOI
(<a href="https://doi.org/10.5281/zenodo.21968992">10.5281/zenodo.21968992</a>, resolves to the
latest archived release); doi.org content negotiation serves APA/Chicago/CSL formats from it.
A machine manifest lives at <a href="/llms.txt">/llms.txt</a>; structured data at
<a href="/registry.json">registry.json</a> and <a href="/registry.csv">registry.csv</a>.</p>
<h3>Maintainer</h3>
<p><a href="https://github.com/srinivasgumdelli">Srinivas Gumdelli</a> - founding editor.
Registration authority currently rests with the editor; conflicts of interest are disclosed
inside the affected records. Each record states who registered it.</p>
<h3>Licensing</h3>
<p>Records and data: CC BY 4.0 (cite PipeRoll and the PIR id). Tooling: MIT.</p>
</div>"""
    os.makedirs(os.path.join(OUT, "about"), exist_ok=True)
    with open(os.path.join(OUT, "about", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PAGE.format(title="About - PipeRoll", css=CSS, home="../index.html",
                             home_prefix="../", h1="About the registry", footer_extra="",
                             sub="What PipeRoll is, how it works, how to cite it",
                             body=about_body))

    # contribute page, rendered from CONTRIBUTING.md
    contrib_md = open(os.path.join(ROOT, "CONTRIBUTING.md"), encoding="utf-8").read()
    contrib_html = markdown.markdown(contrib_md, tab_length=2)
    os.makedirs(os.path.join(OUT, "contribute"), exist_ok=True)
    with open(os.path.join(OUT, "contribute", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PAGE.format(title="Contribute - PipeRoll", css=CSS, home="../index.html",
                             home_prefix="../", h1="Contributing to PipeRoll", footer_extra="",
                             sub="Open data, open submissions, verified registration",
                             body=f'<div class="record">{linkify(contrib_html)}</div>'))

    # data & formats page - the deliberate doorway to machine-readable data
    data_body = """<div class="record">
<p>All registry data is open (CC BY 4.0). These are the machine-readable surfaces;
each is regenerated from the records on every change.</p>
<h3>Formats</h3>
<ul>
<li><a href="../registry.json">registry.json</a> - every record's structured fields
(normalized taxonomy keys first). For analysis code.</li>
<li><a href="../registry.csv">registry.csv</a> - the same, flat. Loads directly into
pandas or a spreadsheet. Your browser may download rather than display it.</li>
<li>Per-record markdown - append <code>.md</code> to any record permalink
(e.g. <code>/pir/2026-0045.md</code>) for the raw source-of-truth record.</li>
<li><a href="../llms.txt">/llms.txt</a> - machine manifest for LLM agents
(llmstxt.org convention) with links to every record's markdown.</li>
<li><a href="https://doi.org/10.5281/zenodo.21968992">Zenodo archive (DOI)</a> - versioned
snapshots of the entire registry; doi.org content negotiation serves APA/Chicago/BibTeX/CSL
citations from it.</li>
<li><a href="https://github.com/piperoll/registry">GitHub repository</a> - full history,
schema, and the verification pipeline.</li>
</ul>
<p>Statistics caveat: counts are a floor, not a frequency estimate - see
<a href="../about/">About</a> for the completeness disclosure.</p>
</div>"""
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    with open(os.path.join(OUT, "data", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PAGE.format(title="Data and formats - PipeRoll", css=CSS, home="../index.html",
                             home_prefix="../", h1="Data &amp; formats", footer_extra="",
                             sub="Machine-readable surfaces of the registry",
                             body=data_body))

    # llms.txt - machine manifest (llmstxt.org convention)
    lines = ["# PipeRoll - Agent Incident Registry", "",
             "> Verified public records of AI-agent failures: what the agent controlled,",
             "> what went wrong, what it cost, and what the evidence is. Counts are a floor,",
             "> not a frequency estimate; absence from the registry is not evidence of safety.",
             "",
             "- Structured data: https://piperoll.org/registry.json and https://piperoll.org/registry.csv",
             "- Schema: https://github.com/piperoll/registry/blob/main/incident-schema-v0.md",
             "- Contribute: https://piperoll.org/contribute/",
             "- Archived releases DOI: https://doi.org/10.5281/zenodo.21968992",
             "- Each record has a raw markdown endpoint at its permalink + '.md'",
             "", "## Records", ""]
    for r in sorted(records, key=lambda x: x["id"]):
        lines.append(f"- [{r['id']}: {cut(r.get('title',''), 80)}]"
                     f"(https://piperoll.org/pir/{r['id'].replace('PIR-','').lower()}.md)")
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"built {len(records)} records -> docs/")


if __name__ == "__main__":
    build()
