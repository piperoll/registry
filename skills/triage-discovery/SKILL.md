---
name: triage-discovery
description: Use to work through the registry's open `discovery` issues end to end - build the triage sheet, decide every lead with the triage-lead rules, hand the in-scope ones to register-incident or enrich-incident, then close each issue with a per-lead outcome. Runs the mechanical parts with discovery/triage_issues.py; never drafts a record itself, never merges.
---

# Triage the discovery issues

Agent-agnostic: no tool names. A human can follow it by hand. This is the
daily loop that keeps the `discovery` label at zero open issues; it wraps
`triage-lead` (the judgement) with `discovery/triage_issues.py` (the
mechanics) so the judgement is the only part anyone spends time on.

## 0. Ground truth

- `skills/triage-lead/SKILL.md` - the scope tests and the three verdicts.
- `skills/register-incident/SKILL.md`, `skills/enrich-incident/SKILL.md` -
  what to do with a `register` or `enrich` verdict.
- `CONTRIBUTING.md`, `AGENTS.md`, `CONSTITUTION.md` - the rules the skills
  point at.

## 1. Build the sheet

```
python3 discovery/triage_issues.py sheet --json /tmp/triage.json
```

The sheet lists every open discovery issue and every lead in it, and
pre-classifies the cheap cases with a written reason:

- `registered` - the lead's URL or title already matches a record (the ids
  are named). Verdict is `enrich` only if the lead carries new evidence;
  otherwise it is a reject with "already registered: PIR-...".
- `advisory` - a GitHub security advisory. A vulnerability in agent tooling
  with no deployed exposure shown is out of scope; this is most leads.
- `quote-or-roundup` - a quote post, a release note, a weekly recap. Not an
  incident. If it points at one, follow the pointer and triage *that*.
- `REVIEW` - everything else. These need the `triage-lead` test.

Read the pre-classified ones quickly anyway: the rules are cheap, not
infallible. An advisory that describes a deployed exploitation is still in
scope; move it to review.

## 2. Decide every REVIEW lead

Apply `triage-lead` to each: who acted, what failed, is it registered, is
there a primary. Write the verdict into the lead's `outcome` field in the
JSON in one of these shapes, so the closing comment reads the same way for
every lead across every day:

- `out of scope: <reason>` - the reason names the test that failed (the
  subject is not an agent; the agent did what its operator intended; a
  pre-release eval in simulation with no third party; product news).
- `already registered: PIR-YYYY-NNNN` - optionally `; enriched via PR #N`.
- `registered as PIR-YYYY-NNNN (<short title>), PR #N` - after step 3.
- `held: <what would flip it>` - rare; use when a primary is pending (an
  investigation update, an attribution) and name the trigger.

### Before any reject: the five checks the 2026-11-03 audit added

An audit of every closed discovery issue (Aug to Nov 2026) found false
rejections with a common cause: a shortcut, not a judgement. Run these
before writing any `out of scope` outcome.

1. **Open every roundup.** A weekly recap or newsletter is never
   `commentary` unread. Triage each item inside it on its own. (The Sep 21
   recap closed in #71 hid Plugin4Shell.)
2. **Judge against the registry, not the article's framing.** "All attempts
   failed" or "no access gained" describes a near-miss, which is in scope.
   Check how the closest existing record was classified before rejecting.
   (#88 was rejected on "failed and unattributed" while PIR-2026-0075 had
   registered the same swarm's failed probes; it became 0114 to 0116.)
3. **Sweep every target a primary names**, not only the one that triggered
   the lead. A researcher report that lists five targets is five leads.
   (Transluce's Data USA and university-library episodes went untriaged
   for six weeks.)
4. **Weigh a dispute; don't count it.** A first-person account with
   artifacts is corroborable at low-to-medium confidence (PIR-2026-0038,
   0051, 0113). An unsupported counter-claim, such as a Community Note
   resting on the reporter's commercial interest, lowers confidence; it does
   not make the account unregistrable.
5. **When a scope rule changes, re-run it on existing records.** A rule
   tightened for new leads but never applied backwards leaves records that
   would now be rejected (0061 and 0084 were withdrawn on 2026-11-03 for
   this reason).

## 3. Draft the in-scope leads first, then close

A `register` or `enrich` verdict goes through its skill and ends in a pull
request **before** the issue is closed, so the closing comment can cite the
PR and the id. Group records from one disclosure stream (one operator, one
announcement, several victims) into one PR and say why in its description;
otherwise one record per PR.

Two things the daily loop keeps tripping on:

- **Self-incidents.** When the operator in the lead is the lab that made the
  model doing the drafting, the record's rule-4 disclosure is the strongest
  the registry has, every fact must trace to a named source, and the PR must
  ask for review by a model from another lab or a human before merge.
- **Dates from fetch summaries.** A summary can pair a real number with the
  wrong label (an incident report's title date read as the outage date; a
  reporter's name attached to someone else's article). Read the primary or
  its machine-readable form before any date or figure enters a record.

## 4. Close

```
python3 discovery/triage_issues.py close /tmp/triage.json --dry-run   # read the comments
python3 discovery/triage_issues.py close /tmp/triage.json
```

`close` refuses to close an issue that still has a lead without an
outcome, posts one comment per issue listing every lead's outcome, and
closes it. The comments are the audit trail of what the registry declined
and why; they are as important as the records it accepted.

## What good looks like

Zero open `discovery` issues; every closed one carries a per-lead outcome a
reader can check against the scope test; every in-scope lead is a PR with
the sources it was verified against; nothing drafted from a summary alone.
