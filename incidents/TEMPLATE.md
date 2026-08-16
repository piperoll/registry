# PIR-YYYY-NNNN - One-line title: what failed and what it cost

<!-- Use the next free id (check INDEX.md); the year is the registration year.
     Filename must equal the id. Delete all comments before submitting.
     Every enum field must START with exactly one canonical token from
     incident-schema-v0.md (v0.2 lists); nuance goes in prose after it. -->

- `id`: PIR-YYYY-NNNN
- `title`: Fuller restatement of the failure
- `date_occurred`: YYYY-MM-DD (or YYYY-MM / YYYY / "not applicable - researcher demonstration")
- `date_detected`: relative is fine ("same session", "~3 weeks")
- `date_disclosed`: when it became public
- `status`: corroborated | disputed | draft

### The agent
- `agent_description`: what the system is, one paragraph
- `operator_type`: individual | startup | enterprise | autonomous | unknown
- `autonomy_level`: human-approves-each-action | human-on-the-loop | autonomous-within-policy | fully-autonomous
- `model_stack`: model(s) + versions if known
- `harness`: the scaffolding, if known

### Authority
- `authority_scope`: what the agent could touch (funds, credentials, code execution, comms, data)
- `funds_at_risk_usd`: maximum exposed at incident time
- `blast_radius`: one machine | one org | customers/third parties | public | fleet/systemic

### The failure
- `root_cause`: one primary token; contributing causes in prose
- `failure_locus`: agent-reasoning | harness | tool-mcp | dependency | model-provider | operator-config | unknown
- `exploitation_status`: in-wild-exploited | in-wild-malfunction | in-wild-payload-failed | researcher-demonstrated | bounty-game | unknown
- `mechanism`: the causal chain, step by step
- `adversary_present`: yes | no | unknown

### Impact
- `severity`: near-miss | degraded | loss | catastrophic
- `direct_loss_usd`: realized, not exposed; ranges with basis stated; "unknown" is honest
- `indirect_loss_usd`:
- `downtime`:
- `data_exposure`:

### Detection and recovery
- `detected_by`: operator | agent-self | third-party | automated-monitor | platform-automated | attacker-disclosure
- `time_to_detect`:
- `time_to_recover`:
- `remediation`:
- `structural_fix`: rule/architecture change made, or "none"
- `controls_that_worked`: functioning controls that bounded the loss

### Evidence
- `telemetry_grade`: none | operator-logs | append-only | witnessed
- `sources`: full https:// URLs only, each one you actually opened (one per sub-bullet)
  - `independence`: how independent the sources are of each other and of the operator
- `confidence`: low | medium | high, with the weakest link named
