---
name: enrich-incident
description: Use when new evidence - a fresh investigation, technical report, forensic analysis, court development, or additional source - arrives about an incident that is already registered. Adds it to the existing record with a dated verification note, never rewrites history silently, and opens a pull request for human review. Never merges.
---

# Enrich an existing incident record

Agent-agnostic: no tool names. A human can follow it by hand.

New evidence about a registered incident is **not a new record**. The
registry's ids are permanent and its records are append-only in substance: a
record grows a documented history rather than being quietly replaced. This
skill keeps that discipline while letting a record deepen as the world learns
more.

## 0. Read the canonical rules first

- `AGENTS.md` - hard rules; in particular: *never edit the substance of an
  existing record silently*; factual changes require a dated line.
- `CONTRIBUTING.md` and `incident-schema-v0.md` for fields and format.

## 1. Confirm it is an enrichment, not a new record

Search `incidents/*.md` and `incidents/INDEX.md` for the event. If the
incident is registered, you are enriching that record. If it is genuinely a
different incident (different event, even if the same actors), use the
`register-incident` skill instead. When one source covers both an existing
incident and a new one, split the work: enrich the existing record and
register the new one separately.

## 2. Verify the new evidence against its primary

Same discipline as registering: a summary of the new report is a lead, not a
fact. Fetch and read the new source itself (Internet Archive if the page
blocks automated fetching - and say so). Establish who published it and
whether it is genuinely **independent** of the parties already cited (a new
independent investigation strengthens the record; a re-report of an existing
source does not).

## 3. Record what changed, with a dated note - never silently

Every substantive addition gets a dated line in the record's verification /
corrections section, in the form:

```
- YYYY-MM-DD: expanded from <source> (<date>). Added <what>. No prior claim
  was retracted.   <- or: Corrected <prior claim> to <new claim> because <why>.
```

Rules:

- **Never retract or alter a prior claim without saying so.** If the new
  evidence contradicts something in the record, state the contradiction, say
  which source is more authoritative and why, and either correct the claim
  (with the dated line) or record it as a discrepancy deliberately not
  adopted. A reader must be able to see the record's history.
- Attribute the new facts to the new source, in the record's own voice
  ("Per <source>, ..."), not as unqualified truth.
- Keep speculation and editorial narrative out; record what the source
  establishes.

## 4. Update the record's fields

- Add the source to `sources` with: who published it, its date, what it
  establishes, and that it was read (and how, if via an archive).
- Fold the key new facts into the relevant field - usually `mechanism`,
  sometimes `data_exposure`, `remediation`, `time_to_detect`, or `severity`.
  Add a paragraph attributed to the new source rather than rewriting existing
  prose.
- If the new source is a genuinely new independent party, upgrade the
  `independence` note and say why.
- Revisit `confidence` honestly if the new evidence changes it.

## 5. Validate

```
python3 tools/validate.py incidents/PIR-YYYY-NNNN.md   # must show 0 errors
python3 tools/build.py                                  # must not error
```

## 6. Open a pull request - never merge

- Branch, never `main`. **One record per PR** (an enrichment is one logical
  change).
- The PR description says what evidence was added, from which primary, how
  it was verified, whether any prior claim was corrected or retracted, and
  any conflict of interest.
- **Do not merge, do not enable auto-merge, do not bypass checks.** Merge
  authority is editorial and human.
- **The PR must be approved by the repository's code owner** (see
  `CODEOWNERS`) before it merges. Your job ends when the PR is open, green,
  and its description says what changed and how it was verified. See
  `skills/README.md` for the full pipeline.

## What good looks like

Someone reading the record a year later can see exactly when each piece of
evidence arrived, from whom, and what it changed - and can tell an addition
from a correction from a deliberately-not-adopted discrepancy.
