# Discovery pipeline

A daily job that surfaces **candidate agent-incident leads** for editorial review.
It gathers from configured sources, scores each lead against the registry's scope,
dedupes against the published registry, and writes survivors to `../candidates/`.

**It never registers a record and never edits `incidents/`.** Discovery feeds
verification; it does not replace it. The registry's value is that every record is
individually verified against primary sources - a scraper that auto-published would
destroy that. So this pipeline produces leads only; a human turns a lead into a
record through the normal intake + verification flow.

## Run

```
python3 discovery/discover.py            # gather, triage, write candidates/<date>.md
python3 discovery/discover.py --dry-run  # print candidates, write nothing
```

stdlib only - no external dependencies, no secrets required. `GITHUB_TOKEN` (if
present) raises the GitHub advisory API rate limit but is optional.

## How it works

- **`sources.py`** - one function per source, each returning
  `{title, url, date, summary, source}`. Included: `github_advisories`
  (GitHub-reviewed security advisories, keyword-filtered) and `rss`
  (security-outlet feeds, stdlib-parsed). `websearch` is a documented stub -
  Actions runners have no WebSearch tool, so wire a search-API provider (key via
  secret) to enable it. Every source is best-effort: a dead feed logs a warning
  and yields nothing, never crashing the run.
- **`triage.py`** - `scope_score` applies the "subject is always an agent" rule as
  a cheap keyword pass (agent/LLM subject + incident language, minus
  product/funding-news penalties); `triage` drops anything already in the
  registry (`docs/registry.json` titles) or in `candidates/seen.txt`, keeps leads
  at or above `min_score`, and ranks them.
- **`discover.py`** - orchestrates and writes `candidates/<date>.md` plus the
  running `seen.txt`. Dedup reads the records straight from `incidents/` (the
  source of truth, always present), not the built `docs/registry.json`.
- **Output**: the workflow does not commit to the repo (main is protected and
  verified-only). It uploads `candidates/<date>.md` as a run **artifact** and
  opens one **triage issue** (label `discovery`); `seen.txt` persists across runs
  via the Actions cache. Promotion of a lead to a record is a human PR into
  `incidents/`.
- **`config.json`** - sources, keyword lists, `min_score`. Tune here.

## Tuning

Start conservative (write to `candidates/`, review by hand). Once the false-positive
rate is acceptable, options to consider: raise cadence, add the `websearch` source
with a provider key, or have the workflow open a pre-filled intake issue per lead
instead of writing a file. Do not shortcut verification.
