"""Candidate-lead sources for the discovery pipeline.

Each source returns a list of raw candidate dicts:
    {"title": str, "url": str, "date": "YYYY-MM-DD"|None, "summary": str, "source": str}

stdlib only (urllib + xml.etree) - no external deps, so the pipeline runs on a
bare runner. Every source is best-effort: a fetch failure yields [] and a logged
warning, never a crash, so one dead feed cannot sink a daily run.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

UA = "piperoll-discovery/0.1 (+https://piperoll.org)"


def _get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _warn(msg):
    print(f"warn  discovery.sources: {msg}", file=sys.stderr)


def _recent(date_str, max_age_days):
    if not date_str or max_age_days is None:
        return True
    try:
        d = datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return True  # undated: keep, let triage/dedup decide
    return d >= datetime.now(timezone.utc) - timedelta(days=max_age_days)


def github_advisories(cfg):
    """Recent GitHub-reviewed security advisories, filtered by keyword.

    Public endpoint; unauth works (low rate limit). In Actions, pass a token via
    GITHUB_TOKEN for headroom. Keyword filter is applied locally on summary text.
    """
    kws = [k.lower() for k in cfg.get("keywords", [])]
    per_page = cfg.get("per_page", 100)
    max_age = cfg.get("max_age_days")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"https://api.github.com/advisories?type=reviewed&sort=published&per_page={per_page}"
    out = []
    try:
        data = json.loads(_get(url, headers))
    except (urllib.error.URLError, ValueError, TimeoutError) as e:
        _warn(f"github_advisories fetch failed: {e}")
        return out
    for a in data:
        summ = (a.get("summary") or "") + " " + (a.get("description") or "")
        low = summ.lower()
        if kws and not any(k in low for k in kws):
            continue
        pub = (a.get("published_at") or "")[:10] or None
        if not _recent(pub, max_age):
            continue
        out.append({
            "title": a.get("summary") or a.get("ghsa_id") or "advisory",
            "url": a.get("html_url") or a.get("url") or "",
            "date": pub,
            "summary": (a.get("description") or "")[:500],
            "source": "github-advisories",
            "cve": a.get("cve_id"),
        })
    return out


def _text(el):
    return "".join(el.itertext()).strip() if el is not None else ""


def rss(cfg):
    """RSS 2.0 and Atom feeds, parsed with stdlib. Returns recent items."""
    max_age = cfg.get("max_age_days")
    out = []
    for feed in cfg.get("feeds", []):
        try:
            raw = _get(feed)
            root = ET.fromstring(raw)
        except (urllib.error.URLError, ET.ParseError, ValueError, TimeoutError) as e:
            _warn(f"rss fetch/parse failed for {feed}: {e}")
            continue
        # RSS: channel/item ; Atom: feed/entry
        items = root.findall(".//{*}item") or root.findall(".//{*}entry")
        for it in items:
            title = _text(it.find("{*}title"))
            link_el = it.find("{*}link")
            link = ""
            if link_el is not None:
                link = link_el.get("href") or _text(link_el)
            date = (_text(it.find("{*}pubDate")) or _text(it.find("{*}updated"))
                    or _text(it.find("{*}published")))
            date_norm = None
            m = re.search(r"(\d{4})-(\d{2})-(\d{2})", date)
            if m:
                date_norm = m.group(0)
            else:
                m = re.search(r"(\d{1,2})\s+(\w{3})\s+(\d{4})", date)  # RFC822-ish
                if m:
                    try:
                        date_norm = datetime.strptime(m.group(0), "%d %b %Y").strftime("%Y-%m-%d")
                    except ValueError:
                        pass
            if not _recent(date_norm, max_age):
                continue
            summ = _text(it.find("{*}description")) or _text(it.find("{*}summary"))
            out.append({
                "title": title, "url": link, "date": date_norm,
                "summary": re.sub(r"<[^>]+>", "", summ)[:500],
                "source": f"rss:{re.sub(r'^https?://(www\\.)?', '', feed).split('/')[0]}",
            })
    return out


def websearch(cfg):
    """Stub. Actions runners have no WebSearch tool; wire a search-API provider
    (key via secret) to enable. Disabled by default so the pipeline needs no
    secrets. Returns [] unless implemented."""
    if not cfg.get("enabled"):
        return []
    _warn("websearch source enabled in config but not implemented - skipping")
    return []


REGISTRY = {"github_advisories": github_advisories, "rss": rss, "websearch": websearch}


def gather(config):
    items = []
    for name, fn in REGISTRY.items():
        scfg = (config.get("sources") or {}).get(name) or {}
        if not scfg.get("enabled"):
            continue
        got = fn(scfg)
        print(f"  source {name}: {len(got)} raw items")
        items += got
    return items
