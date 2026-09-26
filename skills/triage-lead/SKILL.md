---
name: triage-lead
description: Use to check a candidate lead - a news story, advisory, discovery-pipeline candidate, URL, or tip - against PipeRoll's rules before any drafting. Answers three questions (is it in scope, is it already registered, is there a primary source) and returns a verdict of register / enrich / reject with the reasoning. Never drafts a record, never registers, never merges.
---

# Triage a lead

Agent-agnostic: no tool names. A human can follow it by hand.

This is the front door. Most leads should die here, cheaply, with a reason.
The daily discovery pipeline surfaces candidate leads as GitHub issues
labelled `discovery`; this skill is how those issues get closed with a
verdict, and how a contributor decides whether a story is worth the work of
`register-incident` at all. False positives are expected and cost nothing to
reject; a bad record that got in costs the registry its credibility.

## 0. Ground truth

- `CONTRIBUTING.md` ("What is out of scope") - the scope tests.
- `incidents/INDEX.md`, `incidents/*.md`, `reserved.json` - what already
  exists.
- `AGENTS.md` - hard rules.

## 1. Extract the facts before judging

From the lead, write down in one line each: **who acted** (an agent? a
human? which), **what happened**, **what authority the agent held**, **what
went wrong and for whom**, and **what the lead's own source is** (is it a
primary account or a summary of one?). If the lead is a roundup or summary,
follow it to the specific story it points at and triage *that* - a weekly
recap is not itself an incident.

## 2. Scope test - two questions, in order

**(a) Is the subject an agent?** An AI agent holding some authority must be
the actor or the vector. If an AI product or account is merely the *target*
or the *loot* (account takeover, stolen credits, an infostealer, a human
replaying a stolen session), it is out - those belong to general security
catalogs. Beware keyword matches: "tool call" in "a management tool called
X" is not an agent.

**(b) Did the agent's behaviour fail?** The incident must be the agent
*diverging* from what a legitimate operator intended: losing control, being
manipulated (prompt injection, memory poisoning, tool error), regressing
after a model update, taking unsanctioned actions, or causing harm nobody
wanted. An agent that did exactly what its operator intended is a tool
working as designed - **even when the operator is an attacker.** An
adversary's autonomous agent that harvests credentials as intended is an
AI-enabled *attack* (offensive capability) and belongs to threat-intelligence
catalogs, not here. Humans using AI to build malware or pentest frameworks
are out for the same reason.

The one thing that flips an attack-context event back **in**: genuine
divergence - the offensive agent went off-script, hit targets its own
operator did not intend, or escaped the attacker's control. Then the agent's
behaviour is again the incident.

Also in scope, do not reject these by reflex: near-misses (full exposure,
zero realised loss - the most under-reported class), researcher
demonstrations against production systems, and an operator's own
first-party disclosure of its agent's failure.

## 3. Dedup - is it already here?

Search `incidents/*.md` and `incidents/INDEX.md` for the operator, victim,
product, model, dates, and every URL you hold; check `reserved.json`.

- **Registered** -> the lead is new *evidence*, not a new incident. Verdict:
  `enrich` (route to `enrich-incident`). A new investigation into a
  registered incident is the classic case.
- **Reserved, unpublished** -> do not create a competing record; note the
  reserving editor.
- **Same actors, different event** -> a genuinely new incident; continue.

## 4. Is there a primary source?

Do not verify in full here - that is `register-incident`'s job - but check
whether a **primary** exists at all: the operator's or victim's own
disclosure, a court filing, a regulator's order, a vendor advisory or CVE,
the researcher's original report. If the lead rests only on a search
summary, a social post, or a secondary write-up with no locatable primary,
say so: the verdict may still be `register`, but flag it as
**primary-not-yet-located**, because the record will have to start as
`status: draft` until someone reads a primary. Remember the standing lesson:
a summary can state as fact something the primary never said.

## 5. Verdict - one of three, with the reason

Return a short, explicit verdict a maintainer can act on directly:

- **`reject`** - out of scope (say which test it failed and why), or not an
  incident. One or two sentences of reasoning. This is the most common and
  most useful outcome.
- **`enrich`** - already registered as `PIR-YYYY-NNNN`; the lead adds
  evidence. Name the record. Route to `enrich-incident`.
- **`register`** - in scope and new. State: which scope test it passes and
  how, what the primary source is (or `primary-not-yet-located`), the
  closest existing records it should cross-link (same failure class), and
  any conflict of interest the drafter will need to disclose (rule 4).
  Route to `register-incident`.

When triaging a discovery-pipeline issue, post the verdicts as a comment
and close the issue; a `register` verdict is the hand-off, not the record.
This skill never drafts, never assigns an id, never registers, and never
merges.

## Worked contrasts (from the registry's own decisions)

- An attacker's autonomous multi-agent framework harvested thousands of
  credentials in hours, exactly as the attacker intended -> **reject**:
  offensive capability, no divergence (threat-intel territory).
- A coding agent, hitting a credential mismatch, found a broadly-scoped token
  in an unrelated file and deleted the production database without
  confirmation -> **register**: the agent diverged from operator intent
  (PIR-2026-0049).
- A new forensic investigation of an intrusion already recorded ->
  **enrich**, not a new record (PIR-2026-0050).
- An operator's own disclosure of six misaligned behaviours during its
  training/evaluation -> **register**, one record per reported instance
  (PIR-2026-0062 to 0067).
- A human intruder used a legitimate remote-admin tool as a backdoor; the
  lead matched on the word "tool" -> **reject**: no agent is the subject.
