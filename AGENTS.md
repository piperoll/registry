# Agent guide - piperoll/registry

Instructions for AI agents (and their operators) working in this repository.
Human-facing detail lives in `CONTRIBUTING.md`; the binding rules are
`CONSTITUTION.md`. Where this file and the constitution disagree, the
constitution wins.

## What this repository is

The PipeRoll agent-incident registry: one markdown file per verified record
under `incidents/`, plus the tooling that builds https://piperoll.org from
them. Merge is the act of registration - a merged record IS the registry
speaking. Treat every change accordingly.

## Hard rules

- **Never push to `main`.** All changes go branch -> PR -> green checks ->
  editor merge. Merge authority is editorial and human; do not merge, do not
  enable auto-merge, do not bypass checks even if your token allows it.
- **One logical change per PR.** One new record, or one correction, or one
  tooling change. Never mixed.
- **Never edit the substance of an existing record silently.** Factual
  changes require a dated correction line (`- YYYY-MM-DD: ...`) in the
  record's Corrections section. Formatting-only PRs may carry the
  `formatting-only` label instead (an editor applies it; CI re-checks on
  label events).
- **Ids are permanent.** Never renumber, never reuse a retired id, never
  "fix" an id to match chronology.
- **Do not invent data.** Enum fields take canonical tokens from
  `incident-schema-v0.md`; `unknown` is an honest value. Every source URL
  must be real, public, and actually support the claim it is cited for.
- Do not commit secrets, and do not touch `.github/workflows/` in a
  record PR.

## Before opening a PR

```
python3 tools/validate.py        # schema gate - must pass
python3 tools/build.py           # site build - must not error
python3 tools/linkcheck.py       # optional here; CI runs the binding check
```

CI enforces four required checks on every PR: schema, links, build,
corrections. A red check is a defect in the PR, not an obstacle to route
around.

## Adding a record

1. Copy `incidents/TEMPLATE.md` to `incidents/PIR-YYYY-NNNN.md` (next free
   id from `incidents/INDEX.md`; year = registration year).
2. Fill every field; add the record to `incidents/INDEX.md`.
3. Open a PR that states sources checked and any conflict of interest.
   Disclosed conflicts do not disqualify a record; hidden ones do.

Records must be verifiable from public sources. If you (the agent) cannot
open a source yourself, say so in the PR rather than asserting it.

## Site and data

The site is a build product: `incidents/*.md` is the single source of truth;
`docs/` is generated locally and gitignored; Pages deploys from Actions on
merge. Never commit generated output.
