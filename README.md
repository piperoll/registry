# PipeRoll - Agent Incident Registry

Verified public records of AI-agent failures: what the agent controlled, what went wrong,
what it cost, and what the evidence is. Named for the Pipe Rolls - the English Exchequer's
great rolls, 676 unbroken years of audited records kept tamper-evident by a parallel copy
in different hands.

**Live site**: https://piperoll.org

## Principles

- Every record is verified individually against primary sources before publication.
- Corrections are published in the record, never slipped.
- Rejected candidates retire their reserved ids permanently; ids are never reused (CVE convention).
- Ids are permanent opaque names. The initial import (PIR-2026-0001..0045) was numbered by
  occurrence date as a one-time property; later ids are assigned at registration.
- Near-misses are records too - full exposure with zero realized loss is actuarially precious.

## Layout

- `incidents/` - the records (one markdown file per PIR id) + `INDEX.md`
- `incident-schema-v0.md` - the schema, including its amendment history (v0.1, v0.2)
- `tools/build.py` - static site generator: `python3 tools/build.py` regenerates `docs/`
- `tools/linkcheck.py` - fetch-grade liveness check for every source URL
- `docs/` - the built site (GitHub Pages serves this directory), including
  `registry.json` and `registry.csv` machine-readable exports

## Licensing

Records and registry data: CC BY 4.0 (cite PipeRoll and the PIR id).
Tooling: MIT. The incident schema is open and will remain open.

## Submitting an incident

Open an issue with sources. Records enter the registry only after verification;
submissions without independently checkable sources will not be registered.
