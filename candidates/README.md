# Candidate leads (UNVERIFIED - not registry records)

This directory holds machine-surfaced **candidate leads** from the discovery
pipeline (`discovery/`). They are not records:

- **No PIR id.** Nothing here is registered.
- **Not verified.** These are pointers for editorial review, surfaced by keyword
  heuristics. False positives are expected.
- **Not published.** Nothing in `candidates/` is built into the site
  (`piperoll.org`); the site is built only from verified `incidents/` records.

A lead becomes a record only after a human verifies it against primary sources
and it passes the scope test ("the subject is always an agent" - see
CONTRIBUTING). To register one, open the
[incident intake form](https://github.com/piperoll/registry/issues/new?template=incident-report.yml).

**Where leads go.** The daily job does not commit here (main is protected and
verified-only). Each run instead uploads its `YYYY-MM-DD.md` as a workflow
**artifact** and opens one **triage issue** (label `discovery`) with the leads.
Triage there; promote a real one via the normal PR into `incidents/`. Dedup
state (`seen.txt`) is carried across runs by the Actions cache, so the same lead
is not surfaced twice. This directory holds the seed `seen.txt` and this README;
`YYYY-MM-DD.md` files here are only transient run output.
