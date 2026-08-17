# PipeRoll - Agent Incident Registry

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21968992.svg)](https://doi.org/10.5281/zenodo.21968992)
[![Witnessed](https://img.shields.io/badge/dynamic/json?label=witnessed&query=%24.logIndex&prefix=rekor%20index%20&url=https%3A%2F%2Fpiperoll.org%2Fwitness%2Fprovenance.json&color=2b4a6f)](https://piperoll.org/witness/)

Verified public records of AI-agent failures: what the agent controlled, what went wrong,
what it cost, and what the evidence is. Named for the Pipe Rolls - the English Exchequer's
great rolls, 676 unbroken years of audited records kept tamper-evident by a parallel copy
in different hands.

**Live site**: https://piperoll.org

## Constitution

The registry's binding rules are published as [CONSTITUTION.md](CONSTITUTION.md)
(rendered at [piperoll.org/constitution](https://piperoll.org/constitution/)).
Records cite rules by number; rules are amended by PR and never renumbered.

## Principles

- Every record is verified individually against primary sources before publication.
- Corrections are published in the record, never slipped.
- Rejected candidates retire their reserved ids permanently; ids are never reused (CVE convention).
- Ids are permanent opaque names. The initial import (PIR-2026-0001..0045) was numbered by
  occurrence date as a one-time property; later ids are assigned at registration.
- Near-misses are records too - full exposure with zero realized loss is actuarially precious.

## Completeness disclosure

This registry records what is publicly reported and independently verifiable - a fraction
of what occurs. Most agent failures are never disclosed. Coverage is biased toward the
visible: on-chain losses, court and regulator records, published research, viral
postmortems, and English-language sources; crypto-agent incidents are overrepresented
relative to silent enterprise failures for exactly this reason. The initial 45 records
were gathered by structured research sweeps (Aug 2026), not systematic sampling.
Consequences: registry counts are a floor, never a frequency estimate; absence of a
system from the registry is not evidence of its safety; and no failure *rate* can be
computed from this data alone, because the exposure base - how many agents run, with
what authority - is unknown. Correcting that denominator problem is part of the
institution's roadmap, not a property of this dataset.

## Layout

- `incidents/` - the records (one markdown file per PIR id) + `INDEX.md`
- `incident-schema-v0.md` - the schema, including its amendment history (v0.1, v0.2)
- `tools/build.py` - static site generator: `python3 tools/build.py` regenerates `docs/`
- `tools/linkcheck.py` - fetch-grade liveness check for every source URL
- the site is a build product, not a committed copy: `python3 tools/build.py`
  renders `incidents/*.md` into `docs/` locally (gitignored); CI builds and
  deploys it to Pages on every merge, exports included

## Maintainer

[Srinivas Gumdelli](https://github.com/srinivasgumdelli) - founding editor.
Registration authority currently rests with the editor (see `CONTRIBUTING.md`);
conflicts of interest are disclosed inside the affected records, per the
registry's constitution.

## Licensing

Records and registry data: CC BY 4.0 (cite PipeRoll and the PIR id).
Tooling: MIT. The incident schema is open and will remain open.

## Contributing

Open data, open submissions, verified registration: anyone may submit a record
via PR, CI enforces the schema and checks every source link, verification is
editorial, and merge is the act of registration. See `CONTRIBUTING.md` and
`incidents/TEMPLATE.md`. Merge authority stays with the editors - that split
(Wikipedia intake, CVE authority) is constitutional.
