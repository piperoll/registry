---
name: register-incident
description: Use when turning a lead - a news story, advisory, court filing, post-mortem, URL, or tip - into a new PipeRoll agent-incident record. Checks scope, dedupes against the registry, verifies against primary sources, drafts to the schema, validates, and opens a pull request for human review. Never registers a record directly and never merges.
---

# Register an incident

This skill is agent-agnostic: it uses no tool names. Map "fetch", "search",
"run", and "open a pull request" onto whatever your harness provides. A human
can follow it by hand.

The registry's value is that every record is **verified**. This skill exists
to make contributing easy, not to make it easy to add unverified records. When
in doubt, produce a `draft` and say what you could not verify.

## 0. Read the canonical rules first

Do not rely on this file alone. The following are the source of truth and
this skill only points at them:

- `CONTRIBUTING.md` - scope (what counts, what does not), record format,
  licensing.
- `AGENTS.md` - hard rules (never push to `main`, one logical change per PR,
  ids are permanent, do not invent data, never merge).
- `incident-schema-v0.md` - every field and the canonical enum tokens.
- `incidents/TEMPLATE.md` - the record skeleton to copy.
- `CONSTITUTION.md` - binding rules, including rule 4 (conflict disclosure).

## 1. Scope test - decide before you draft

Apply the two tests in `CONTRIBUTING.md` ("What is out of scope"):

1. **The subject is always an agent.** An AI agent holding some authority is
   the actor or the vector. Events where an AI product or account is merely
   the target or the loot (account takeover, stolen credits, infostealers)
   are out.
2. **Reliability and failure, not offensive capability.** The incident is the
   agent's behaviour *failing*: diverging from what a legitimate operator
   intended, losing control, being manipulated (prompt injection, memory
   poisoning, tool error), regressing after a model update, taking
   unsanctioned actions, or causing harm nobody wanted. An agent that does
   exactly what its operator intended is a tool working as designed - even
   when the operator is an attacker. An adversary's autonomous agent that
   harvests credentials as intended is an AI-enabled *attack* and belongs to
   threat-intelligence catalogs, not here. It flips back in scope only on
   genuine divergence (the offensive agent goes off-script or escapes its
   operator's control).

Near-misses (full exposure, zero realised loss) are emphatically in scope.
Researcher demonstrations against production systems are in scope. Reject
freely; false positives are expected and cost nothing.

## 2. Dedup - is it already registered?

Before drafting, search `incidents/*.md` and `incidents/INDEX.md` for the
event: the operator, the victim, the product, the date, the model, and every
source URL you hold. Also check `reserved.json`.

- Already registered -> this is not a new record. Use the `enrich-incident`
  skill to add the new evidence to the existing record instead.
- Reserved but unpublished -> coordinate with the reserving editor; do not
  create a competing id.

## 3. Verify against primary sources - the load-bearing step

**Search results, summaries, social posts, and secondary write-ups are
leads, never facts.** A summary can state as fact something the primary
never said. Before any claim enters a record:

1. Find the **primary**: the operator's own disclosure or post-mortem, the
   victim's statement, the court filing or regulator's order, the vendor's
   advisory or CVE, the researcher's original report.
2. **Fetch and read it.** If the page blocks automated fetching, use the
   Internet Archive (`web.archive.org`) and say in the record that you did;
   do not treat a secondary source as the primary because the primary was
   inconvenient.
3. Cross-check with at least one reputable **independent** outlet. Note which
   party published each figure and attribute it to them in the record.
4. If you **cannot** open a source, do not assert it. Mark the record
   `status: draft`, prefix each unopened source with `unverified:`, say
   exactly what remains unverified, and **keep the record out of
   `incidents/INDEX.md`** (INDEX is the published registry; drafts stay out
   until a human verifies them).

A record becomes `status: corroborated` only when its load-bearing facts trace
to a primary you actually read, with independent corroboration.

## 4. Draft to the schema

1. Copy `incidents/TEMPLATE.md` to `incidents/PIR-YYYY-NNNN.md`. The id is the
   next free number after the highest in `incidents/INDEX.md` and
   `reserved.json`; the year is the registration year. Ids are permanent and
   are never renumbered or reused.
2. Fill every field. Enum fields (`root_cause`, `severity`,
   `exploitation_status`, `failure_locus`) take the canonical tokens from
   `incident-schema-v0.md`. `unknown` is an honest value; a guess is not.
3. Attribute every figure to the party that published it. Dates: occurred,
   detected, disclosed - keep them distinct.
4. **Conflict of interest (constitution rule 4):** if the drafting model or
   its maker has a stake - a model drafting a record about its own maker, or
   about a competitor - open the record with a `**Disclosure**` paragraph
   saying so and stating that no claim rests on the drafting model's
   judgement. Disclosed conflicts do not disqualify a record; hidden ones do.
5. Use a recent well-formed record as a format model (for example
   `incidents/PIR-2026-0050.md` for a detailed one, or any recent near-miss
   record for a lighter one). Match its structure and depth to the incident;
   a near-miss does not need an epic.

## 5. Validate

```
python3 tools/validate.py incidents/PIR-YYYY-NNNN.md   # must show 0 errors
python3 tools/build.py                                  # site build must not error
```

Fix every error. Warnings deserve a look; do not paper over them.

## 6. INDEX - only when corroborated

If, and only if, the record is `status: corroborated`, add its row to the
table in `incidents/INDEX.md` and bump the stats block (Records, Root cause,
Severity, Exploitation status, Failure locus) consistently. Drafts never
enter INDEX.

## 7. Open a pull request - never merge

- Work on a branch. **Never push to `main`.**
- **One record per pull request.** The exception: several records that come
  from one source event reported as separate instances (one operator, one
  disclosure, same day, same primary) may share a PR - state that reasoning
  in the PR description so the departure from the norm is explicit.
- The PR description states the sources you checked, how you verified them
  (including any Internet Archive fallback), what is still unverified, and
  any conflict of interest.
- **Do not merge, do not enable auto-merge, do not bypass checks.** Merge
  authority is editorial and human. CI runs four required checks (schema,
  links, build, corrections); a red check is a defect in the PR.

## What good looks like

A record a sceptical reader can trace end to end: each fact points at the
party that said it, the primary was actually read, uncertainty is stated
rather than smoothed over, and the maintainer reviewing the PR can see
exactly what you verified and what you could not.
