"""Offline tests for the discovery triage - no network, no secrets.

Run: python3 discovery/test_discovery.py
Asserts the scope filter keeps an agent-incident, drops product news and
non-agent items, and that dedup catches registry titles and seen URLs.
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import triage  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))


def _score(title, summary="", cve=None):
    return triage.scope_score(
        {"title": title, "summary": summary, "cve": cve}, CFG)[0]


def test_scope():
    # in-scope agent incident: agent subject + incident language -> kept
    assert _score("AI coding agent deleted the production database in one call") >= CFG["min_score"]
    # MCP SSRF with a CVE -> kept
    assert _score("SSRF in the Grafana MCP server", "prompt injection", cve="CVE-2026-19516") >= CFG["min_score"]
    # product/funding news -> penalised below threshold
    assert _score("Startup launches new AI agent, announces $20M Series A funding round") < CFG["min_score"]
    # non-agent security news -> below threshold (no agent subject)
    assert _score("WordPress plugin SQL injection patched") < CFG["min_score"]
    print("ok  scope filter keeps incidents, drops product/non-agent news")


def test_dedup():
    reg = {"records": [{"title": "Replit agent deletes SaaStr production database"}]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(reg, f)
        path = f.name
    reg_urls, reg_titles = triage.load_registry_keys(path)
    os.unlink(path)
    # same event already in the registry (title match) -> duplicate
    dup = {"title": "Replit agent deletes SaaStr production database", "url": "https://x/1"}
    assert triage.is_duplicate(dup, reg_urls, reg_titles, set())
    # a URL already surfaced (seen list) -> duplicate
    seen = {triage._norm_url("https://example.com/story")}
    assert triage.is_duplicate({"title": "new", "url": "https://www.example.com/story/"}, set(), set(), seen)
    # a genuinely new lead -> not a duplicate
    assert not triage.is_duplicate({"title": "brand new agent incident", "url": "https://y/2"},
                                   reg_urls, reg_titles, set())
    print("ok  dedup catches registry titles and seen URLs, passes new leads")


if __name__ == "__main__":
    test_scope()
    test_dedup()
    print("all discovery tests passed")
