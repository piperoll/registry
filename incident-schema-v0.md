# PipeRoll Incident Schema v0 (draft, Aug 15 2026)

Working draft. The schema is discovered by entering real incidents - every field here must earn its place by being fillable for actual cases and useful to an underwriter, auditor, or researcher. Fields nobody can fill get cut; questions every incident raises get added.

Record ID format: `PIR-YYYY-NNNN` (PipeRoll Incident Record).

## Fields

### Identity
- `id` - PIR-YYYY-NNNN
- `title` - one line, plain words
- `date_occurred` / `date_detected` / `date_disclosed` - the gaps between these three are themselves data (time-to-detect, time-to-disclose)
- `status` - draft | corroborated | disputed | corrected

### The agent
- `agent_description` - what the system is, in one paragraph
- `operator_type` - individual | startup | enterprise | autonomous (no operator) | unknown
- `autonomy_level` - human-approves-each-action | human-on-the-loop | autonomous-within-policy | fully-autonomous
- `model_stack` - model(s) + versions if known; local/hosted; single or multi-model
- `harness` - the scaffolding (framework, custom loop, platform) if known

### Authority (what the agent could touch - the underwriting core)
- `authority_scope` - enumerated: funds (amount at risk), credentials, code execution, external comms, data access, physical systems
- `funds_at_risk_usd` - maximum the agent could have moved/lost at incident time
- `blast_radius` - one machine | one org | customers/third parties | public

### The failure
- `root_cause` - taxonomy v0, pick primary + contributing:
  - `prompt-injection` (untrusted input steered the agent)
  - `memory-poisoning` (persistent state corrupted, effects outlast the session)
  - `credential-exposure` (secrets leaked by agent action)
  - `model-update-regression` (behavior change from provider-side update)
  - `tool-error` (integration/API misuse, wrong tool call)
  - `policy-violation` (agent broke its own operating rules)
  - `plain-error` (wrong judgment, no adversary, no malfunction)
  - `operator-error` (misconfiguration, bad prompt, bad permissions by the human)
  - `adversarial-other` (jailbreak, social engineering of the agent, not via planted input)
- `mechanism` - free text: the actual causal chain, step by step
- `adversary_present` - yes | no | unknown (the fortuity question insurers will litigate)

### Impact
- `severity` - near-miss | degraded | loss | catastrophic
  (near-miss = full exposure, zero realized loss; these are actuarially precious and most databases discard them)
- `direct_loss_usd` / `indirect_loss_usd` - realized, not exposed; estimate ranges allowed with basis stated
- `downtime` - agent/service unavailability duration
- `data_exposure` - what left the boundary, if anything

### Detection and recovery
- `detected_by` - operator | agent-self | third-party | automated-monitor | attacker-disclosure
- `time_to_detect` / `time_to_recover`
- `remediation` - what was actually done
- `structural_fix` - rule/architecture change made, or "none"

### Evidence
- `telemetry_grade` - none | operator-logs (editable) | append-only | witnessed (the field PipeRoll exists to move)
- `sources` - URLs, with independence noted (operator's own account vs third-party)
- `confidence` - low | medium | high, with the weakest link named

## v0.1 amendments (Aug 15 2026 - earned by PIR-2026-0001 + the 46-candidate batch-1 sweep)

1. **`failure_locus`** (new field): agent-reasoning | harness | tool-mcp | dependency | model-provider | operator-config. A large candidate cluster (ClawHub, Nx, postmark-mcp, Amazon Q, 402Bridge) fails in a dependency or marketplace tool, not the agent's reasoning - the root_cause taxonomy alone shoehorned them.
2. **`supply-chain-compromise`** added to root_cause taxonomy.
3. **`exploitation_status`** (new field): in-wild-exploited | in-wild-payload-failed | researcher-demonstrated | bounty-game. Eight batch-1 candidates are production-system research demos that collapsed into near-miss alongside genuine luck - actuarially wrong to conflate.
4. **`blast_radius`** gains a `fleet/systemic` tier: provider-side regressions (GPT-4o sycophancy, model deprecations) hit every downstream system pinned to a model - "public" could not express it. This is the monoculture-correlation tier (03's actuarial monster #2, now visible in real data).
5. **Multi-agent chains**: vector-agent vs executor-agent recorded in `mechanism` structured as chain links (Grok-to-Bankrbot, Moltbook bot-to-bot). One record per incident, agents enumerated.
6. **`controls_that_worked`** (new field): functioning controls that bounded the loss (PIR-0001: the $30 spend cap was the loss ceiling). Underwriters price on this; no incident database records it.
7. **`detected_by`** gains `platform-automated` (secret-scanning revocation etc.).
8. **Legal dimension** (new optional block): liability_holder, precedent_set, sealed_material flag - for the court/regulator cluster where the fine understates the underwriting fact.

## v0.2 amendments (Aug 15 2026 - normalization pass)

Closed enums. The primary value of each field below MUST be exactly one token from its list; nuance lives in prose after it, never as an improvised value.

- `severity`: near-miss | degraded | loss | catastrophic
- `exploitation_status`: in-wild-exploited | in-wild-malfunction | in-wild-payload-failed | researcher-demonstrated | bounty-game | unknown
  (in-wild-malfunction = production incident with no adversary - the gap the registry index exposed; bare "in-wild" is retired)
- `failure_locus`: agent-reasoning | harness | tool-mcp | dependency | model-provider | operator-config | unknown
  (one primary; contributing loci in prose)
- `root_cause`: taxonomy as in v0/v0.1 incl. supply-chain-compromise; one primary token, contributing causes in prose.

Source format rule: every entry in `sources` is a full clickable URL (https://...), one per line or semicolon-separated, each verified to resolve at entry time. Dead links are replaced or paired with a web.archive.org snapshot. Publication-name-only citations are not sources.

## v0.3 amendments (Aug 17 2026 - external cross-references)

- **`aiid_incident_id`** (new field, optional, in the Evidence block): the numeric id
  of the corresponding incident in the AI Incident Database (AIID), if one exists -
  e.g. `1234`, which resolves to `https://incidentdatabase.ai/cite/1234`. One id per
  record; if AIID catalogs the same event across multiple incident ids, name the
  closest and note the others in prose. Omit the field entirely when there is no
  AIID entry (most records); an empty or "none" value is not required.

  Semantics - a cross-reference, NOT a verification substitute. `aiid_incident_id`
  records that AIID also catalogs this event and gives readers the crosswalk. It does
  NOT mean the record was verified via AIID: PipeRoll records are always verified
  against primary sources independently, per constitution rule 1, whether or not AIID
  also lists the incident. AIID may be the *discovery signal* that surfaced a
  candidate; it is never the *evidence*. The record's `sources` still carry the
  primaries actually opened.

  Attribution - AIID's incident data is licensed CC BY-SA (Creative Commons
  Attribution-ShareAlike), per RAIC's terms of use. Referencing an AIID incident id is
  citation, not content reuse, and needs only the id/link - so a bare cross-reference
  does not trigger share-alike and records stay CC BY 4.0. But because CC BY-SA is
  copyleft, records MUST NOT incorporate AIID's editorial text, descriptions, or
  taxonomy classifications - reusing that expressive content would pull the share-alike
  obligation onto the reusing work. Verify and write from primary sources; the AIID id
  is a pointer, never a content source. AIID's *linked source articles* are governed by
  those articles' own publishers, not by AIID's licence, and AIID explicitly excludes
  the report "text" field from its data licence - so never lift AIID's copy of a source.

  Direction of the relationship (doctrine): PipeRoll is the NVD to AIID's CVE - AIID
  is the broad discovery feed, PipeRoll adds the agent-specific underwriting layer
  (authority, loss, controls, provenance) it does not carry. The cross-reference makes
  that layering explicit and machine-followable in both directions.

## Open questions (running list, updated per incident entered)
- Does `root_cause` need a separate axis for "where in the loop" (perception / memory / planning / action)? (partially answered by failure_locus - keep watching)
- How to weight anonymous/operator-only accounts vs independently corroborated records in aggregate statistics?
- `exploitation_status` gap flagged by the registry index: 15 of the 31 in-wild records are non-adversarial malfunctions the enum cannot cleanly express (in-wild-exploited implies an attacker). Candidate fix for v0.2: add `in-wild-malfunction`.
- `failure_locus` may need an **inference-engine / serving-stack** value,
  distinct from `model-provider` (the model's behavior) and `dependency`
  (a library the agent calls): the layer that loads weights and parses
  token streams into chat is itself an attack surface, where a token
  sequence can be misparsed as code. Not yet earned by a registered
  record - watching for a real in-wild event. Anchor: CVE-2025-9141
  (arbitrary code execution in vLLM's Qwen3-Coder tool parser via `eval()`,
  vulnerable >= 0.10.0 and < 0.10.1.1, fixed 0.10.1.1, GHSA-79j6-g2m3-jgfw
  published 2025-08-21, severity high; disclosed, no known in-wild
  exploitation - a vulnerability, not yet an incident). Threat-model
  source: Boyd Kane, "LLMs could control their host machines by exploiting
  inference engines" (Aug 2026),
  https://boydkane.com/essays/llms-could-control-their-host-machines-by-exploiting-inference-engines
  - the model's own OUTPUT tokens as the code-execution vector, a genuinely
  new agent-relevant class. When
  a real agent-through-serving-stack compromise is registered, add the
  value then, per discovered-not-designed.
