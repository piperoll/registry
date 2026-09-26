# Contribution pipeline - end to end

One lead becomes one verified record through four stages. Each stage hands
off to the next; nothing skips a stage, and nothing lands on `main` without
the code owner's approval. The skills are harness-agnostic (no tool names):
Claude Code, Codex, Cursor, any other agent, or a human can run them.

```
 discovery (automated)  ->  triage-lead  ->  register-incident / enrich-incident  ->  code-owner approval  ->  merge
     daily cron               verdict           validated record + pull request         a human, in the PR UI     site rebuilds
```

## Stage 0 - Discovery (automated, daily)

`discovery/` runs on a cron (no model, no LLM key - a deterministic keyword
triage over security advisories and feeds). It surfaces **candidate leads**
as GitHub issues labelled `discovery`, uploads the candidate list as a run
artifact, and never writes a record or touches `main`. See
`discovery/README.md`. A lead can also arrive by hand: a story, a tip, a URL.

## Stage 1 - Triage: `triage-lead`

Check every candidate against the rules before anyone drafts anything:
is the subject an agent, did its behaviour fail (reliability, not offensive
capability), is it already registered, is there a primary source. Return
one of three verdicts with the reasoning:

- `reject` - most leads end here, cheaply. Post the verdict and close the
  discovery issue.
- `enrich` - already registered as `PIR-YYYY-NNNN`; the lead is new evidence.
  Hand off to `enrich-incident`.
- `register` - in scope and new. Hand off to `register-incident`, naming the
  primary source (or `primary-not-yet-located`), the records to cross-link,
  and any conflict of interest to disclose.

`triage-lead` never drafts, never assigns an id, never registers.

## Stage 2 - Draft: `register-incident` or `enrich-incident`

- **New incident:** `register-incident` - dedup, read the **primary** (Archive
  fallback if bot-blocked), draft to the schema with rule-4 disclosure,
  validate, add to INDEX only if `corroborated`, open a pull request.
- **Existing incident:** `enrich-incident` - read the new source, add it with
  a dated verification note, never rewrite history silently, validate, open a
  pull request.

Both end in a pull request on a branch. **Neither merges.** If a source
cannot be opened, the record stays `status: draft` with `unverified:`
sources and out of INDEX, and the PR says exactly what is unverified.

## Stage 3 - Approval and merge (human, code owner)

Every pull request must be **approved by the repository's code owner** (see
`CODEOWNERS`) before it merges, and merging is the editor's act. CI must be
green on the four required checks (schema, links, build, corrections); a red
check is a defect in the PR, not something to route around. Agents do not
merge, do not enable auto-merge, and do not bypass checks - even if their
token would allow it. On merge, the site rebuilds from `main` automatically.

## The rules behind the skills

The skills point at the canonical files and do not restate them. On any
disagreement the canonical file wins and the skill is the bug:

- `CONTRIBUTING.md` - scope and format
- `AGENTS.md` - hard rules
- `incident-schema-v0.md` - fields and enum tokens
- `incidents/TEMPLATE.md` - the record skeleton
- `CONSTITUTION.md` - binding rules, including rule 4 (conflict disclosure)
- `CODEOWNERS` - who must approve a merge
