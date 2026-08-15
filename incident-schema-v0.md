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

## Open questions (running list, updated per incident entered)
- Does `root_cause` need a separate axis for "where in the loop" (perception / memory / planning / action)? (partially answered by failure_locus - keep watching)
- How to weight anonymous/operator-only accounts vs independently corroborated records in aggregate statistics?
- `exploitation_status` gap flagged by the registry index: 15 of the 31 in-wild records are non-adversarial malfunctions the enum cannot cleanly express (in-wild-exploited implies an attacker). Candidate fix for v0.2: add `in-wild-malfunction`.
