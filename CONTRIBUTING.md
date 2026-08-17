# Contributing to PipeRoll

PipeRoll is open data with verified registration: anyone can submit, only verified
records enter, and merge authority stays with the editors. That split is
constitutional - the registry's only asset is never being wrong in public.

## Submitting without code

Not a developer, or no time for the PR flow? Use the
[incident report form](https://github.com/piperoll/registry/issues/new?template=incident-report.yml) -
a structured GitHub issue. Editors (and, in time, a triage agent) turn qualifying
reports into records through the same verification gates; you are credited as the
reporting party via the issue. Reports need public, checkable sources; conflicts
must be disclosed and do not disqualify you - hiding them does.

Reading a postmortem or news story you want to flag? This bookmarklet opens the
form prefilled with the page you are on - drag it to your bookmarks bar:

    javascript:(()=>{window.open('https://github.com/piperoll/registry/issues/new?template=incident-report.yml&title='+encodeURIComponent('[incident] '+document.title)+'&sources='+encodeURIComponent(location.href))})()

## Submitting an incident

1. Copy `incidents/TEMPLATE.md` to `incidents/PIR-YYYY-NNNN.md` using the next free
   id (check `incidents/INDEX.md`; the year is the current registration year).
2. Fill every field. Enum fields must start with one canonical token from
   `incident-schema-v0.md`. "unknown" is an honest value; an invented figure is not.
3. Sources: full https URLs you actually opened, independent where possible.
   Publication names are not sources. First-party accounts are welcome but say so.
4. Open a PR. Disclose any conflict of interest (you are the operator, a
   competitor, an insurer of the subject, etc.) in the PR description -
   conflicted submissions are accepted, undisclosed conflicts are not.

## What happens to your PR

- **CI (automatic)**: schema validation, fetch-grade link check on your sources,
  and a clean site build. Red CI will not be reviewed.
- **Verification (editorial)**: claims are checked against sources adversarially -
  possibly assisted by an LLM verification agent posting its findings on the PR.
  Expect corrections; dates and dollar figures move under scrutiny more often
  than submitters expect.
- **Merge = registration.** A merged record gets its id permanently; rejected
  reserved ids are retired and never reused. Editors' decisions on registration
  are final; disagreements are welcome as issues on the record afterward.

## Corrections to existing records

PRs against the record file, with sources. Corrections are published in the
record, never silently - and CI enforces it (constitution rule 2): any PR
that modifies an existing record must add a dated entry to that record's
Corrections or Verification notes section, in the form:

    - 2026-09-03: direct_loss_usd revised from ~50,000 to 62,400 per the
      operator's amended filing (https://...).

Editors may waive the gate for mechanical sweeps (mass reformatting, link
canonicalization) by applying the `formatting-only` label - the label is
itself an auditable editorial act. If your correction changes a date, the id
does not change - identity and chronology are deliberately decoupled (see the
id policy in `incidents/INDEX.md`).

## For LLM agents

If you are an AI agent preparing a submission, work from raw sources, not the
rendered site:

- Machine manifest: https://piperoll.org/llms.txt (links every record's raw markdown)
- Schema (read the amendments - enums are closed):
  https://raw.githubusercontent.com/piperoll/registry/main/incident-schema-v0.md
- Record template:
  https://raw.githubusercontent.com/piperoll/registry/main/incidents/TEMPLATE.md
- Structured data for dedup checks: https://piperoll.org/registry.json

Before opening a PR: confirm the incident is not already registered (check
registry.json titles and dates), fill every field or write "unknown" - never
invent a value to complete a field - and run `python3 tools/validate.py` plus
`python3 tools/linkcheck.py <your-PIR-id>` locally; CI runs both. State in the
PR description that the submission is agent-authored and name your operator -
that is a conflict-of-interest disclosure, not a barrier: agent-authored
submissions are welcome and verified exactly like any other.

## What is out of scope

Hypotheticals, vendor marketing scenarios, undisclosed-conflict hit pieces,
and vulnerabilities with no deployed system exposed (pure research on toy
targets). Researcher demonstrations against production systems are in scope
and recorded as `researcher-demonstrated`. Near-misses are emphatically in
scope - full exposure with zero realized loss is the most underreported class
of incident and among the most actuarially useful.
