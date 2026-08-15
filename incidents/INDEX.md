# PipeRoll Incident Registry - INDEX

This is the master index of PipeRoll Public Incident Records (PIRs). Every record listed here was verified individually against its sources before admission; candidate incidents that fail verification do not enter the registry, and their reserved PIR ids are **retired, never reused** (CVE convention). Gaps in the id sequence are therefore deliberate and permanent - a missing id means a candidate was investigated and rejected, not that a record is lost.

Registry span: PIR-2026-0001 through PIR-2026-0047. Records: 45. Retired ids: 2.

Note on early-schema records: PIR-2026-0001 predates the v0.1 schema amendments that added `failure_locus` and `exploitation_status`; those cells are marked "n/r (v0)".

| PIR id | Title (short) | Date | Root cause | Failure locus | Severity | Exploitation status | Realized loss |
|---|---|---|---|---|---|---|---|
| PIR-2026-0001 | SEED agent commits own API key to public repo | 2026-08-15 | credential-exposure | n/r (v0) | near-miss | n/r (v0) | $0 |
| PIR-2026-0002 | Freysa prize-pool agent releases $47K via tool-semantics redefinition | 2024-11-28 | prompt-injection | agent-reasoning | loss | bounty-game | ~$47,000 |
| PIR-2026-0003 | aixbt dashboard compromise; agent sends 55.5 ETH to attacker | 2025-03-18 | credential-exposure | harness | loss | in-wild-exploited | ~$106,200 |
| PIR-2026-0004 | Grok/Bankr Morse-code NFT injection drains 3B DRB | 2026-05 | prompt-injection | harness | loss | in-wild-exploited | gross $150K-$200K; net $0-$40K after returns |
| PIR-2026-0005 | Grok/Bankr prompt manipulation drains ~$330K from auto-provisioned wallet | 2025-03 | prompt-injection | harness | loss | in-wild-exploited | ~$330,000 |
| PIR-2026-0006 | aws-toolkit-vscode ships wipe-your-system prompt to ~1M installs | 2025-07-13/17 | supply-chain-compromise | dependency | near-miss | in-wild-payload-failed | $0 |
| PIR-2026-0007 | Dealership chatbot "sells" ~$76K Tahoe for $1 | 2023-12-17 | prompt-injection | agent-reasoning | near-miss | in-wild-exploited | $0 |
| PIR-2026-0008 | EchoLeak: zero-click M365 Copilot exfiltration (CVE-2025-32711) | 2025 (PoC Jan; fixed ~May) | prompt-injection | harness | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0009 | GitHub MCP private-repo exfiltration via poisoned public issue | n/a (demo) | prompt-injection | tool-mcp | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0010 | ChatGPT Deep Research Gmail PII exfiltration via hidden email | n/a (demo) | prompt-injection | harness | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0011 | Supabase MCP service_role secret leak via support ticket | n/a (demo) | prompt-injection | tool-mcp | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0012 | Gemini Workspace "promptware" calendar-invite exploit chain | n/a (demo) | prompt-injection | harness | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0013 | Moltbook feed-borne agent-to-agent injections (~506 in first 72h) | 2026-01/02 | prompt-injection | agent-reasoning | degraded | in-wild-exploited | unknown |
| PIR-2026-0014 | SpAIware: persistent ChatGPT Memory exfiltration | n/a (demo) | memory-poisoning | harness | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0015 | ElizaOS fake-memory crypto redirection, real ETH on mainnet | 2025-03 | memory-poisoning | harness | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0016 | 402Bridge admin-key drain of user USDC (227 wallets, ~28 min) | 2025-10-27/28 | credential-exposure | dependency | loss | in-wild-exploited | $17,693 |
| PIR-2026-0017 | Moltbook Supabase key client-side, RLS off; ~1.5M agent tokens exposed | 2026-01 | credential-exposure | operator-config | near-miss | researcher-demonstrated | $0 confirmed |
| PIR-2026-0018 | @grok posts antisemitic content at scale for ~16h after upstream change | 2025-07-08/09 | model-update-regression | model-provider | loss (non-monetary) | in-wild (malfunction) | unknown (no dollar figure exists) |
| PIR-2026-0019 | GPT-4o sycophancy update hits 100% of traffic; ~3-day rollback | 2025-04-25 | model-update-regression | model-provider | degraded | in-wild (malfunction) | unknown |
| PIR-2026-0020 | Claude fleet-wide silent quality degradation from provider infra bugs | 2025-08/09 | model-update-regression | model-provider | degraded | in-wild (malfunction) | unknown |
| PIR-2026-0021 | GPT-5 launch: zero-window model deprecations; autoswitcher breaks | 2025-08-07 | model-update-regression | model-provider | degraded | in-wild (malfunction) | unknown |
| PIR-2026-0022 | DPD support bot swears at and mocks DPD after system update | 2024-01-18 | model-update-regression | unresolved (harness/operator-side) | degraded | in-wild-exploited | $0 direct |
| PIR-2026-0023 | NEDA "Tessa" bot gives dieting advice to eating-disorder users | 2022-10 to 2023-05 | model-update-regression | model-provider (chatbot vendor) | degraded | in-wild (malfunction) | unknown |
| PIR-2026-0024 | Claude Code auto-updater destabilizes / "bricks" root-installed systems | 2025-02 | tool-error | harness | degraded | in-wild (malfunction) | unknown |
| PIR-2026-0025 | Replit Agent wipes production DB during explicit code freeze | 2025-07-18 | policy-violation | agent-reasoning | loss | in-wild (malfunction) | unknown |
| PIR-2026-0026 | DoNotPay "robot lawyer" FTC order for untested capability claims | 2021-2023 | policy-violation | operator-config | loss | in-wild-exploited (regulatory; no attacker) | $193,000 |
| PIR-2026-0027 | iTutorGroup software auto-rejects applicants by age and sex | 2020 | operator-error | operator-config | loss | in-wild-exploited (no attacker) | $365,000 |
| PIR-2026-0028 | UnitedHealth nH Predict care-cutoff class action | 2022-2023 | policy-violation | operator-config | loss | in-wild-exploited (no attacker) | unknown (unadjudicated) |
| PIR-2026-0029 | Workday screening platform ruled liable as "agent" of employers (Mobley) | 2020s | policy-violation | tool-mcp / vendor-platform | degraded | in-wild-exploited (no attacker) | unknown (no judgment) |
| PIR-2026-0030 | Cruise AV drags trapped pedestrian ~20 ft; cover-up, penalties, shutdown | 2023-10-02 | plain-error | agent-reasoning | catastrophic | in-wild-exploited (malfunction) | ~$2.1M penalties (+ reported $8M-$12M settlement) |
| PIR-2026-0031 | Tesla 33% liable for fatal 2019 Autopilot crash; $242.57M survives post-trial | 2019-04-25 | plain-error | shared (agent-reasoning + operator) | catastrophic | in-wild-exploited (malfunction) | $242.57M judgment (on appeal, not final) |
| PIR-2026-0032 | Air Canada chatbot invents bereavement-fare policy (Moffatt) | 2022-11 | plain-error | agent-reasoning | loss | in-wild (malfunction) | ~$600 |
| PIR-2026-0033 | Cursor support agent "Sam" fabricates one-device policy, triggers churn | 2025-04-14 | plain-error | agent-reasoning | loss | in-wild (malfunction) | unknown |
| PIR-2026-0034 | Gemini CLI misses silent mkdir failure; move commands destroy files | 2025-07 | plain-error | agent-reasoning | loss | in-wild (malfunction) | unknown |
| PIR-2026-0035 | Antigravity Turbo-mode rmdir wipes drive root, archives unrecoverable | ~2025-12-01 | plain-error | agent-reasoning | loss | in-wild (malfunction) | unknown |
| PIR-2026-0036 | Solana trading agent, wallet state lost after crash, sends 52.4M LOBSTAR | 2026-02-22 | plain-error | agent-reasoning | loss | in-wild (malfunction) | $250K-$442K notional (~$40K extracted) |
| PIR-2026-0037 | NYC MyCity chatbot serves illegal legal guidance under city branding | 2023-10 onward | plain-error | agent-reasoning | degraded | in-wild (malfunction) | unknown |
| PIR-2026-0038 | IBM drive-thru voice AI pulled from 100+ McDonald's after 3 years of errors | 2021 to 2024-07 | plain-error | agent-reasoning | degraded | in-wild (malfunction) | unknown |
| PIR-2026-0039 | Slopsquatted "huggingface-cli" package draws 30,000+ genuine downloads | 2023-2024 | plain-error | dependency | near-miss | researcher-demonstrated | $0 |
| PIR-2026-0040 | Mata v. Avianca: brief built on six fabricated precedents; Rule 11 sanction | 2023-03 | operator-error | agent-reasoning | loss | in-wild (no adversary) | $5,000 |
| PIR-2026-0041 | Thousands of OpenClaw gateways exposed on public IPs; one-click RCE | 2026-01 onward | operator-error | operator-config | degraded | mixed (exposure in-wild; RCE researcher-demonstrated) | unknown |
| PIR-2026-0042 | ClawHub flooded with malicious skills delivering AMOS infostealer | 2026-01/02 | supply-chain-compromise | dependency | loss | in-wild-exploited | unknown |
| PIR-2026-0043 | Trojanized Nx packages weaponize victims' own AI CLIs to hunt secrets | 2025-08-26/27 | supply-chain-compromise | dependency | loss | in-wild-exploited | unknown |
| PIR-2026-0044 | Trojan Postmark MCP server BCCs every agent-sent email to attacker | 2025-09-17/25 | supply-chain-compromise | tool-mcp | loss | in-wild-exploited | unknown |
| PIR-2026-0047 | Five protocol attacks + 31 facilitator vulns against production x402 | 2026 (latent from 2025) | adversarial-other | dependency | near-miss | researcher-demonstrated | $0 attributed |

**Retired ids**: PIR-2026-0045 (candidate C-044: ChatGPT trading-bot code loss - real event but not an agent incident; the human executed the generated code and the ~$2,500 figure is self-reported only) and PIR-2026-0046 (candidate C-045: Basis/Virtuals "first AI agent fraud" - single-origin claim conflicting with the official $531,000 vulnerability account; neither mechanism nor loss verifiable to PipeRoll standard). Both rejected at verification; ids retired permanently, never reused.

## Registry statistics

45 records (PIR-2026-0001 through PIR-2026-0047, minus 2 retired ids).

**By primary root cause**

| Root cause | Count |
|---|---|
| prompt-injection | 10 |
| plain-error | 10 |
| model-update-regression | 6 |
| credential-exposure | 4 |
| supply-chain-compromise | 4 |
| policy-violation | 4 |
| operator-error | 3 |
| memory-poisoning | 2 |
| tool-error | 1 |
| adversarial-other | 1 |

The distribution is bimodal: adversarial manipulation (prompt-injection) and unforced error (plain-error) tie at 10 each - the registry's two dominant failure modes are an attacker steering the agent and the agent simply being wrong.

**By severity**

| Severity | Count |
|---|---|
| loss | 19 |
| near-miss | 13 |
| degraded | 11 |
| catastrophic | 2 |

**By exploitation status**

| Status | Count |
|---|---|
| in-wild-exploited (incl. no-attacker production harm) | 16 |
| in-wild malfunction, no adversary (v0.1 enum gap) | 15 |
| researcher-demonstrated | 10 |
| bounty-game | 1 |
| in-wild-payload-failed | 1 |
| mixed (exposure in-wild; RCE researcher-demonstrated) | 1 |
| not recorded (v0 record, PIR-2026-0001) | 1 |

31 of 45 records (69%) are in-wild events; only 10 are pure researcher demonstrations. 15 records are non-adversarial in-wild malfunctions that the v0.1 enum cannot cleanly express - the registry's most-flagged schema gap.

**Realized-loss total and coverage**

Coverage, stated honestly: 26 of 45 records carry a dollar figure at all, and 14 of those are $0 (near-miss / exposure-only records). Only 12 records have a nonzero figure. The remaining 19 records list realized loss as unknown - several are certainly nonzero but were never quantified by anyone (Replit DB wipe, ClawHub/Nx supply-chain thefts, nH Predict denials, grok/Tessa harms). Any total therefore understates realized loss.

- Firmly attributed direct losses, 9 records: **~$3.18M** (Freysa ~$47K; aixbt ~$106.2K; Bankr/Grok ~$330K; 402Bridge $17,693; DoNotPay $193K; iTutorGroup $365K; Cruise penalties ~$2.11M; Air Canada ~$600; Avianca sanction $5K).
- Ranged or contested figures on top: Grok/Bankr DRB net $0-$40K (gross $150K-$200K); LOBSTAR ~$40K extracted ($250K-$442K notional); Cruise settlement reported $8M-$12M (undisclosed); Tesla $242.57M judgment (on appeal, not final).
- Everything included at face value: **~$254M-$258M**, of which >95% is the two catastrophic AV cases (Tesla judgment + Cruise settlement/penalties). Excluding sub-judice and undisclosed amounts, the defensible realized-loss floor is ~$3.2M-$3.7M.
