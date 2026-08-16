# Contributing to PipeRoll

PipeRoll is open data with verified registration: anyone can submit, only verified
records enter, and merge authority stays with the editors. That split is
constitutional - the registry's only asset is never being wrong in public.

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
record's verification notes, never silently. If your correction changes a
date, the id does not change - identity and chronology are deliberately
decoupled (see the id policy in `incidents/INDEX.md`).

## What is out of scope

Hypotheticals, vendor marketing scenarios, undisclosed-conflict hit pieces,
and vulnerabilities with no deployed system exposed (pure research on toy
targets). Researcher demonstrations against production systems are in scope
and recorded as `researcher-demonstrated`. Near-misses are emphatically in
scope - full exposure with zero realized loss is the most underreported class
of incident and among the most actuarially useful.
