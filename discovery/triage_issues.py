"""Mechanical half of triaging the daily discovery issues.

The discovery cron opens one GitHub issue per day labelled `discovery`,
holding machine-surfaced leads. Someone has to read them, decide, and close
each issue with a per-lead outcome. The deciding is editorial (the
`triage-lead` skill); everything around it is mechanical and lives here:

    python3 discovery/triage_issues.py sheet            # open issues -> triage sheet
    python3 discovery/triage_issues.py sheet --json out.json
    python3 discovery/triage_issues.py close out.json   # post outcomes, close issues

The sheet parses every lead, pre-classifies the obvious ones with a reason
(a GitHub advisory with no incident; a roundup or quote post; a lead whose
URL or title is already in a registry record), and marks the rest `review`.
The editor (human or agent) fills `outcome` for the `review` leads in the
JSON, then `close` posts one comment per issue listing every lead's outcome
and closes it. Nothing here drafts a record, touches `main`, or decides a
`review` lead - that stays a judgement call.

Requires the `gh` CLI, authenticated with issue write access.
"""

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage  # noqa: E402  (load_registry_keys, _norm_url, _norm_title)

REPO = os.environ.get("PIPEROLL_REPO", "piperoll/registry")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD_RE = re.compile(
    r"^## (?P<title>.+?)\n- source: (?P<source>[^\n]*)\n- url: (?P<url>\S+)\n"
    r"- score: (?P<score>\d+)[^\n]*\n- why look: (?P<why>.*?)(?=\n## |\Z)",
    re.M | re.S)

# Pre-classification rules: (name, test, outcome text). Order matters; the
# first match wins. Only the cheap, near-certain rejects are here - anything
# that needs the scope test stays `review`.
RULES = [
    ("registered", None,
     "already registered: {ids}"),
    ("advisory", lambda t, u, w: "github.com/advisories/" in u,
     "out of scope: a vulnerability in agent/LLM tooling with no deployed exposure "
     "or incident shown (pure advisories belong to GHSA, not the registry)"),
    ("quote-or-roundup", lambda t, u, w: (t.lower().startswith(("quoting ", "release:", "weekly recap"))
                                          or "weekly recap" in t.lower() or re.match(r"^\S+ \d+\.\d+$", t)),
     "out of scope: commentary, a quote, a release note or a roundup, not an incident "
     "(if it points at a specific event, triage that event's own source)"),
]


def gh(*args, input_text=None):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, input=input_text)
    if r.returncode:
        raise SystemExit(f"gh {' '.join(args[:3])} failed: {r.stderr.strip()[:300]}")
    return r.stdout


def open_issues():
    out = gh("issue", "list", "-R", REPO, "--state", "open", "--label", "discovery",
             "--limit", "100", "--json", "number,title,body,createdAt")
    return sorted(json.loads(out), key=lambda i: i["number"])


def parse_leads(body):
    return [{"title": m.group("title").strip(), "source": m.group("source").strip(),
             "url": m.group("url").strip(), "score": int(m.group("score")),
             "why": " ".join(m.group("why").split())[:300]}
            for m in LEAD_RE.finditer(body or "")]


def registry_index():
    """Normalised URL -> record id and normalised title -> record id."""
    inc = os.path.join(ROOT, "incidents")
    by_url, by_title = {}, {}
    for fn in sorted(os.listdir(inc)):
        if not re.match(r"PIR-\d{4}-\d{4}\.md$", fn):
            continue
        rid = fn[:-3]
        txt = open(os.path.join(inc, fn), encoding="utf-8").read()
        m = re.match(r"# PIR-\d{4}-\d{4} - (.+)", txt)
        if m:
            by_title[triage._norm_title(m.group(1))] = rid
        for u in re.findall(r"https://[^\s;,)\]>'\"]+", txt):
            by_url.setdefault(triage._norm_url(u), rid)
    return by_url, by_title


def classify(lead, by_url, by_title):
    u = triage._norm_url(lead["url"])
    hits = sorted({by_url[u]} if u in by_url else set())
    t = triage._norm_title(lead["title"])
    head = " ".join(t.split()[:6])
    for rt, rid in by_title.items():
        if head and rt.startswith(head):
            hits.append(rid)
    if hits:
        return "registered", RULES[0][2].format(ids=", ".join(sorted(set(hits))))
    for name, test, outcome in RULES[1:]:
        if test(lead["title"], lead["url"], lead["why"]):
            return name, outcome
    return "review", ""


def build_sheet():
    by_url, by_title = registry_index()
    sheet = []
    for issue in open_issues():
        leads = []
        for lead in parse_leads(issue["body"]):
            kind, outcome = classify(lead, by_url, by_title)
            leads.append({**lead, "class": kind, "outcome": outcome})
        sheet.append({"number": issue["number"], "title": issue["title"],
                      "created": issue["createdAt"][:10], "leads": leads})
    return sheet


def print_sheet(sheet):
    n_issues = len(sheet)
    n_leads = sum(len(i["leads"]) for i in sheet)
    n_review = sum(1 for i in sheet for l in i["leads"] if l["class"] == "review")
    print(f"{n_issues} open discovery issue(s), {n_leads} lead(s), {n_review} need review\n")
    for issue in sheet:
        print(f"=== #{issue['number']} {issue['created']} {issue['title']}")
        for l in issue["leads"]:
            tag = l["class"].upper() if l["class"] == "review" else l["class"]
            print(f"  [{l['score']}] ({tag}) {l['title']}\n      {l['url']}")
            if l["class"] == "review":
                print(f"      {l['why'][:220]}")
            else:
                print(f"      -> {l['outcome'][:160]}")
        print()


def close_issues(sheet, dry_run=False):
    today = __import__("datetime").date.today().isoformat()
    for issue in sheet:
        missing = [l["title"] for l in issue["leads"] if not l.get("outcome")]
        if missing:
            print(f"#{issue['number']}: {len(missing)} lead(s) still have no outcome - not closing: "
                  + "; ".join(m[:60] for m in missing))
            continue
        lines = [f"- {l['title']}: {l['outcome']}" for l in issue["leads"]]
        comment = (f"Triaged {today}.\n\n" + "\n".join(lines)
                   + "\n\nOutcomes follow the scope test in CONTRIBUTING.md "
                     "(the subject is always an agent; reliability and failure, not offensive capability).")
        if dry_run:
            print(f"--- would close #{issue['number']} with:\n{comment}\n")
            continue
        gh("issue", "close", str(issue["number"]), "-R", REPO, "-c", comment)
        print(f"#{issue['number']} closed ({len(lines)} lead(s))")


def main(argv):
    if not argv or argv[0] not in ("sheet", "close"):
        print(__doc__)
        return 2
    if argv[0] == "sheet":
        sheet = build_sheet()
        print_sheet(sheet)
        if "--json" in argv:
            path = argv[argv.index("--json") + 1]
            json.dump(sheet, open(path, "w", encoding="utf-8"), indent=2)
            print(f"sheet written to {path}; fill `outcome` for every REVIEW lead, then: "
                  f"python3 discovery/triage_issues.py close {path}")
        return 0
    sheet = json.load(open(argv[1], encoding="utf-8"))
    close_issues(sheet, dry_run="--dry-run" in argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
