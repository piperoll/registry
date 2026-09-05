"""Scope-scoring and dedup for discovery candidates.

The scope rule mirrors CONTRIBUTING ("the subject is always an agent"): a lead is
interesting only if it plausibly involves an AI agent AND reads like an incident,
and is penalised if it reads like routine product/funding news. This is a cheap
keyword pass - a first filter to cut noise, never a verification. Verification is
editorial and happens on the record PR, exactly as today.
"""
import json
import os
import re


def scope_score(item, cfg):
    """Return (score, reasons). Higher = more likely an in-scope agent incident."""
    text = f"{item.get('title','')} {item.get('summary','')}".lower()
    reasons = []
    score = 0

    hit_scope = [t for t in cfg.get("scope_terms", []) if t in text]
    # Hard gate: "the subject is always an agent". With no agent/LLM subject
    # term, this is not an agent incident regardless of CVE or incident
    # language, so it can never be a candidate (a CVE'd app vuln with no agent
    # in the loop belongs to a general CVE feed, not here).
    if not hit_scope:
        return -99, ["no agent/LLM subject - out of scope"]

    hit_incident = [t for t in cfg.get("incident_terms", []) if t in text]
    hit_oos = [t for t in cfg.get("out_of_scope_terms", []) if t in text]

    score = 1
    reasons.append("agent/LLM subject: " + ", ".join(hit_scope[:3]))
    if hit_incident:
        score += 1 + (1 if len(hit_incident) > 1 else 0)
        reasons.append("incident language: " + ", ".join(hit_incident[:3]))
    if item.get("cve"):
        score += 1
        reasons.append(f"has CVE ({item['cve']})")
    if hit_oos and not hit_incident:
        score -= 2
        reasons.append("looks like product/funding news: " + ", ".join(hit_oos[:2]))

    return score, reasons


def _norm_url(u):
    u = re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower())
    return u.rstrip("/").split("?")[0].split("#")[0]


def _norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def load_registry_keys(registry_src):
    """Normalized titles and source URLs already in the registry, for dedup.

    Reads the records directly from an incidents/ directory (the source of
    truth, always present) - not docs/registry.json, which is a build artifact
    absent on a fresh CI checkout. Scanning the markdown also yields the source
    URLs (which the JSON export omits), so a lead can be deduped by URL too.
    Accepts either an incidents/ dir or a registry.json path, for flexibility.
    """
    urls, titles = set(), set()
    if not registry_src or not os.path.exists(registry_src):
        return urls, titles
    if os.path.isdir(registry_src):
        for fn in os.listdir(registry_src):
            if not re.match(r"PIR-\d{4}-\d{4}\.md$", fn):
                continue
            txt = open(os.path.join(registry_src, fn), encoding="utf-8").read()
            m = re.match(r"# PIR-\d{4}-\d{4} - (.+)", txt)
            if m:
                titles.add(_norm_title(m.group(1)))
            for u in re.findall(r"https://[^\s;,)\]>'\"]+", txt):
                urls.add(_norm_url(u))
    else:  # a registry.json export (titles only)
        data = json.load(open(registry_src, encoding="utf-8"))
        for r in data.get("records", []):
            if r.get("title"):
                titles.add(_norm_title(r["title"]))
    return urls, titles


def is_duplicate(item, reg_urls, reg_titles, seen_urls):
    u = _norm_url(item.get("url"))
    if u and (u in reg_urls or u in seen_urls):
        return True
    t = _norm_title(item.get("title"))
    if t and t in reg_titles:
        return True
    # near-title match against registry (prefix overlap on the first 6 words)
    if t:
        head = " ".join(t.split()[:6])
        if head and any(rt.startswith(head) for rt in reg_titles):
            return True
    return False


def triage(items, cfg, registry_src, seen_urls):
    reg_urls, reg_titles = load_registry_keys(registry_src)
    min_score = cfg.get("min_score", 2)
    kept = []
    for it in items:
        if is_duplicate(it, reg_urls, reg_titles, seen_urls):
            continue
        score, reasons = scope_score(it, cfg)
        if score >= min_score:
            it = dict(it, _score=score, _reasons=reasons)
            kept.append(it)
    kept.sort(key=lambda x: -x["_score"])
    return kept
