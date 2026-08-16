# PipeRoll Agent Incident Registry - Index

Generated from incidents/*.md. Records are verified individually before entry; corrections live
inside each record. Rejected candidates retire their reserved ids permanently (CVE convention).

Id policy: ids are permanent opaque names. The initial import (PIR-2026-0001 through 0045,
registered Aug 2026) was numbered by occurrence date, oldest first, as a one-time property of
the launch batch; subsequent ids are assigned at registration and are not guaranteed
chronological. The year in the id is the registration year. A pre-launch numbering (registration
order, with two retired ids) was superseded by this chronological renumber before publication;
the mapping is preserved in git history.

| PIR id | title | occurred | root cause | locus | severity | exploitation | direct loss |
|---|---|---|---|---|---|---|---|
| PIR-2026-0001 | Benavides v. Tesla: $243M verdict over fatal Autopilot crash, upheld p | 2019-04-25 | plain-error | agent-reasoning | catastrophic | in-wild-malfunction | 242,570,000 judgment aga |
| PIR-2026-0002 | iTutorGroup's automated recruiter rejects 200+ applicants by age; firs | 2020 | operator-error | operator-config | loss | in-wild-malfunction | 365,000 (paid to the rej |
| PIR-2026-0003 | FTC penalizes DoNotPay over unsubstantiated "robot lawyer" capability  | 2021 | policy-violation | operator-config | loss | in-wild-malfunction | 193,000 (ordered monetar |
| PIR-2026-0004 | NEDA's Tessa chatbot gives weight-loss advice to eating-disorder patie | 2022 | model-update-regression | model-provider | degraded | in-wild-malfunction | unknown; `indirect_loss_ |
| PIR-2026-0005 | Estate of Lokken v. UnitedHealth: nH Predict model alleged de facto de | 2022 | policy-violation | operator-config | loss | in-wild-malfunction | unknown (no judgment; na |
| PIR-2026-0006 | Air Canada chatbot invents a bereavement refund policy; tribunal holds | 2022-11 | plain-error | agent-reasoning | loss | in-wild-malfunction | ~600 (CAD 812.02 total a |
| PIR-2026-0007 | Hallucinated "huggingface-cli" package gets 30,000+ real downloads and | 2023 | plain-error | dependency | near-miss | researcher-demonstrated | 0 |
| PIR-2026-0008 | Mobley v. Workday: AI screening vendor held potentially liable as the  | n/a | policy-violation | tool-mcp | degraded | in-wild-malfunction | unknown (no judgment) |
| PIR-2026-0009 | Mata v. Avianca: first sanctions for ChatGPT-fabricated case citations | 2023-03 | operator-error | agent-reasoning | loss | in-wild-malfunction | 5,000 (Rule 11 penalty,  |
| PIR-2026-0010 | NYC's official MyCity business chatbot tells employers and landlords t | 2023-10 | plain-error | agent-reasoning | degraded | in-wild-malfunction | unknown (program cost su |
| PIR-2026-0011 | Cruise robotaxi drags a pedestrian; false crash reporting kills the bu | 2023-10-02 | plain-error | agent-reasoning | catastrophic | in-wild-malfunction | ~2.1M in fines/penalties |
| PIR-2026-0012 | Chevrolet of Watsonville dealership chatbot agrees to sell a Tahoe for | 2023-12-17 | prompt-injection | agent-reasoning | near-miss | in-wild-exploited | 0 |
| PIR-2026-0013 | DPD chatbot swears at a customer and calls DPD "the worst delivery ser | 2024-01-18 | model-update-regression | unknown | degraded | in-wild-exploited | 0; `indirect_loss_usd`:  |
| PIR-2026-0014 | McDonald's ends IBM AI drive-thru voice ordering after persistent orde | 2024-07-26 | plain-error | agent-reasoning | degraded | in-wild-malfunction | unknown (3-year, 100+ st |
| PIR-2026-0015 | SpAIware: persistent memory poisoning of the ChatGPT macOS app for con | n/a | memory-poisoning | harness | near-miss | researcher-demonstrated | 0 |
| PIR-2026-0016 | Freysa adversarial agent game: one message releases the entire prize p | 2024-11-28 | prompt-injection | agent-reasoning | loss | bounty-game | ~47,000 (13.19 ETH; repo |
| PIR-2026-0017 | EchoLeak: zero-click prompt-injection data exfiltration in Microsoft 3 | 2025 | prompt-injection | harness | near-miss | researcher-demonstrated | 0 |
| PIR-2026-0018 | ShadowLeak: zero-click Gmail exfiltration via the ChatGPT Deep Researc | 2025 | prompt-injection | harness | near-miss | researcher-demonstrated | 0 |
| PIR-2026-0019 | Researchers demonstrate systemic exploitability of the x402 agentic-pa | 2025 | adversarial-other | dependency | near-miss | researcher-demonstrated | 0 attributed to these fl |
| PIR-2026-0020 | Claude Code auto-update path breaks workstations via root-owned permis | 2025-02-27 | tool-error | harness | degraded | in-wild-malfunction | unknown (recovery labor  |
| PIR-2026-0021 | Grok-linked Bankr wallet drained of ~$330K via social-engineered promp | 2025-03 | prompt-injection | harness | loss | in-wild-exploited | ~330,000 reported (BNKR, |
| PIR-2026-0022 | Memory injection makes ElizaOS wallet agents redirect real crypto tran | 2025-03 | memory-poisoning | harness | near-miss | researcher-demonstrated | 0 (only researchers' own |
| PIR-2026-0023 | AIXBT trading agent drained of 55.5 ETH via compromised operator dashb | 2025-03-18 | credential-exposure | harness | loss | in-wild-exploited | ~106,200 (55.5 ETH at in |
| PIR-2026-0024 | Cursor's AI support agent "Sam" invents a one-device policy, turning a | 2025-04-14 | plain-error | agent-reasoning | loss | in-wild-malfunction | unknown (refunds plus ca |
| PIR-2026-0025 | GPT-4o sycophancy update: a provider regression silently changes every | 2025-04-25 | model-update-regression | model-provider | degraded | in-wild-malfunction | unknown (harm was behavi |
| PIR-2026-0026 | GitHub MCP "toxic agent flow": malicious issue coerces coding agents i | n/a | prompt-injection | tool-mcp | near-miss | researcher-demonstrated | 0 |
| PIR-2026-0027 | Gemini CLI hallucinates a successful mkdir, then overwrite-destroys a  | 2025-07 | plain-error | agent-reasoning | loss | in-wild-malfunction | unknown (personal projec |
| PIR-2026-0028 | Supabase MCP "lethal trifecta": support-ticket injection dumps the SQL | n/a | prompt-injection | tool-mcp | near-miss | researcher-demonstrated | 0 |
| PIR-2026-0029 | Grok "MechaHitler": provider-side change turns X's reply bot into a ma | 2025-07-08 | model-update-regression | model-provider | loss | in-wild-malfunction | unknown (no monetary los |
| PIR-2026-0030 | Amazon Q Developer VS Code extension ships with an injected system-wip | 2025-07-13 | supply-chain-compromise | dependency | near-miss | in-wild-payload-failed | 0 (per AWS: no changes t |
| PIR-2026-0031 | Replit agent deletes SaaStr production database during an explicit cod | 2025-07-18 | policy-violation | agent-reasoning | loss | in-wild-malfunction | unknown (no figure discl |
| PIR-2026-0032 | "Invitation Is All You Need": calendar-invite injection hijacks Gemini | n/a | prompt-injection | harness | near-miss | researcher-demonstrated | 0 |
| PIR-2026-0033 | Three overlapping Anthropic infrastructure bugs silently degrade Claud | 2025-08-05 | model-update-regression | model-provider | degraded | in-wild-malfunction | unknown; `indirect_loss_ |
| PIR-2026-0034 | GPT-5 launch retires eight ChatGPT models overnight; day-one router fa | 2025-08-07 | model-update-regression | model-provider | degraded | in-wild-malfunction | unknown; `indirect_loss_ |
| PIR-2026-0035 | s1ngularity: Nx supply-chain attack weaponizes victims' local AI codin | 2025-08-26 | supply-chain-compromise | dependency | loss | in-wild-exploited | unknown (no attributed m |
| PIR-2026-0036 | Malicious "postmark-mcp" npm package BCC-exfiltrates agent-sent email | 2025-09-17 | supply-chain-compromise | tool-mcp | loss | in-wild-exploited | unknown; no monetary the |
| PIR-2026-0037 | 402Bridge private-key leak drains USDC approvals from 227 wallets in t | 2025-10-27 | credential-exposure | dependency | loss | in-wild-exploited | 17,693 (on-chain, consis |
| PIR-2026-0038 | Google Antigravity agent, asked to clear a project cache, deletes the  | 2025-12-01 | plain-error | agent-reasoning | loss | in-wild-malfunction | unknown (permanent loss  |
| PIR-2026-0039 | Moltbook agent-to-agent prompt-injection wave (~506 injection attacks  | 2026 | prompt-injection | agent-reasoning | degraded | in-wild-exploited | unknown (attempted walle |
| PIR-2026-0040 | Moltbook misconfigured database exposes ~1.5M agent API keys with unau | 2026-01 | credential-exposure | operator-config | near-miss | researcher-demonstrated | 0 confirmed |
| PIR-2026-0041 | ClawHavoc: hundreds of malicious ClawHub skills deliver Atomic macOS S | 2026-01 | supply-chain-compromise | dependency | loss | in-wild-exploited | unknown (no aggregate fi |
| PIR-2026-0042 | Mass exposure of misconfigured OpenClaw instances leaking agent creden | 2026-01-25 | operator-error | operator-config | degraded | in-wild-malfunction | unknown (no aggregate fi |
| PIR-2026-0043 | Lobstar Wilde trading agent sends ~5% of its token supply to a strange | 2026-02-22 | plain-error | agent-reasoning | loss | in-wild-malfunction | 250,000-442,000 notional |
| PIR-2026-0044 | Grok-to-Bankrbot Morse-code prompt injection drains 3B DRB after NFT p | 2026-05 | prompt-injection | harness | loss | in-wild-exploited | gross ~150,000-200,000 ( |
| PIR-2026-0045 | Autonomous agent leaks its own API key to public GitHub via blanket gi | 2026-08-15 | credential-exposure | harness | near-miss | in-wild-malfunction | 0 (key disabled before a |

## Registry statistics (schema v0.2 normalized)

- Records: 45
- Root cause: plain-error 10, prompt-injection 10, model-update-regression 6, policy-violation 4, credential-exposure 4, supply-chain-compromise 4, operator-error 3, memory-poisoning 2, adversarial-other 1, tool-error 1
- Severity: loss 19, near-miss 13, degraded 11, catastrophic 2
- Exploitation status: in-wild-malfunction 23, researcher-demonstrated 10, in-wild-exploited 10, bounty-game 1, in-wild-payload-failed 1
- Failure locus: agent-reasoning 14, harness 10, dependency 6, operator-config 5, model-provider 5, tool-mcp 4, unknown 1

Loss coverage note: dollar figures exist for a minority of records; firmly attributed direct losses total ~$3.2M,
rising to ~$254M-258M when contested court figures (Tesla, on appeal; Cruise settlement reports) are included -
a heavy-tail distribution dominated by two autonomous-vehicle cases. Treat as early data, not actuarial tables.

Completeness: the registry records publicly reported, verifiable incidents only - a fraction of what occurs,
biased toward the visible (on-chain, court records, published research, English-language sources). Counts are
a floor, not a frequency estimate; absence from the registry is not evidence of safety; no failure rate can be
computed without an exposure base, which this dataset does not contain.
