# Infostealer malware is hijacking AI sessions to steal metered usage

date: 2026-09-02

Through late August 2026, commodity infostealer malware - Vidar, LummaC2, StealC,
RedLine, and Acreed on Windows, Atomic Stealer on macOS - sitting on users' own
machines scraped saved credentials, browser cookies, and authentication tokens.
Attackers extracted the stolen session cookies for AI accounts and replayed them
to ride victims' already-authenticated sessions, bypassing MFA and single sign-on
entirely, and burned through the victims' paid usage and credits. Anthropic, whose
Claude accounts were among the targets, force-logged-out affected sessions, removed
stored payment methods, and refunded confirmed fraudulent charges. There was no
breach of the provider's systems; the company stated it had "no reason to believe
this malware is related to Claude, installed through Claude, or related to anything
you did with Claude." The malware lives on the endpoint, so a freshly created
session can be stolen again on the next login until the device is cleaned.

**Why this is a field note, not a registry record.** PipeRoll records incidents
where an AI agent holding authority is the actor or the vector. Here no agent acts:
the AI account is the target and the loot, and the mechanism is ordinary endpoint
malware plus session replay. That places it outside the registry's scope (see the
"the subject is always an agent" note in CONTRIBUTING) and inside the remit of
general catalogs like the AI Incident Database. We note it because it is a genuine
loss signal, not because it earns a PIR id.

**Why it matters anyway.** Two things. First, metered AI usage and agent credits
are now a distinct, valuable, resellable credential class - the credential economy
catching up to AI, and a new loss line anyone underwriting agent operations will
have to price, the way card fraud is priced into payments. Second, it is the
adversarial mirror of a problem every keyed agent fleet already has: a hijacked
session, or the defensive force-logout and key rotation that answers it, is
indistinguishable from an outage in an availability signal. Credential compromise
is an availability-and-integrity problem for agent operations, not only a billing
one. The boundary that would pull a future case into the registry proper: an agent
tricked into exfiltrating the session or credentials, or stolen usage demonstrably
running malicious agents downstream - then the agent activity, not the theft, is
the incident.

Sources: The Register (2026-08-31,
https://www.theregister.com/security/2026/08/31/anthropic-cracks-down-on-hijacked-user-accounts-mining-ai-tokens/5293461);
BleepingComputer
(https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-warns-infostealer-malware-is-hijacking-claude-sessions-to-drain-usage/);
Malwarebytes
(https://www.malwarebytes.com/blog/news/2026/09/infostealers-are-hijacking-claude-accounts-at-users-expense);
SecurityWeek
(https://www.securityweek.com/anthropic-warns-claude-users-of-infostealer-malware-infections/).
