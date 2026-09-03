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

Files: `YYYY-MM-DD.md` is one run's leads; `seen.txt` is the running list of
already-surfaced URLs so the same lead is not proposed twice. Prune freely.
