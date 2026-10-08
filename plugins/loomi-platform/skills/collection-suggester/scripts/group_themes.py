#!/usr/bin/env python3
"""Group search queries into collection themes by the attribute values their matching
products share, and add up the demand behind each theme.

Usage:
  python3 group_themes.py --baseline 56.89 --queries q1.json [q2.json] \
      --profiles profiles.jsonl [--min-shared 2] [--min-sessions 30] [--ignore brand]

  --queries   raw get_discovery_query_performance responses (current and prev_* columns)
  --profiles  output of scripts/preview_summary.py, one JSON line per query, run on a
              product grid call for that query (rows=1 is enough; leave facets on)
  --baseline  overall % change in search sessions for the same window, from
              get_discovery_search_performance (trends.browse_sessions)

Two queries join the same theme when their products share at least --min-shared
dominant facet values (for example category=/men/pants and colors=multi; a category
and its parent count once). Wording is not used. Themes are ranked by combined sessions. For each theme the output gives the
shared values (the starting point for a rule), combined sessions, change against the
baseline, revenue, a session-weighted conversion and bounce rate, and which member
queries are underserved (conversion under 75% of the top-20 median, or bounce over
1.5 times the median).

Queries without a profile are listed under `unprofiled` so you can fetch them.
Standard library only; no network access.
"""
import argparse
import json
import statistics
import sys


def money(v):
    if v is None:
        return 0.0
    return float(str(v).replace("$", "").replace(",", "") or 0)


def pct(v):
    if v is None:
        return None
    return float(str(v).replace("%", "") or 0)


def load_queries(paths):
    rows = {}
    for path in paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for r in (data.get("data") or data).get("rows", []):
            rows[r["query"].strip().lower()] = r
    return rows


def load_profiles(paths):
    profiles = {}
    for path in paths:
        with open(path, encoding="utf-8") as f:
            text = f.read().strip()
        items = [json.loads(line) for line in text.splitlines() if line.strip()] if not text.startswith("[") else json.loads(text)
        for p in items:
            q = ((p.get("source") or {}).get("query") or p.get("query") or "").strip().lower()
            if q:
                profiles[q] = p
    return profiles


def signature(profile, ignore):
    values = set()
    for d in profile.get("dominant") or []:
        value = d["value"] if isinstance(d, dict) else d
        if value.split("=", 1)[0] not in ignore:
            values.add(value)
    return values


def collapse(values):
    """Count a category and its parent as one shared value (keep the deepest path)."""
    cats = [v for v in values if v.startswith("category=")]
    drop = {c for c in cats for d in cats if d != c and d.startswith(c.rstrip("/") + "/")}
    return {v for v in values if v not in drop}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--queries", nargs="+", required=True)
    ap.add_argument("--profiles", nargs="+", required=True)
    ap.add_argument("--baseline", type=float, required=True)
    ap.add_argument("--min-shared", type=int, default=2)
    ap.add_argument("--min-sessions", type=int, default=30)
    ap.add_argument("--ignore", nargs="*", default=["brand"], help="facets not to group on (default: brand)")
    a = ap.parse_args()

    rows = load_queries(a.queries)
    profiles = load_profiles(a.profiles)
    growth = 1 + a.baseline / 100

    top = sorted(rows.values(), key=lambda r: r.get("browse_sessions") or 0, reverse=True)[:20]
    med_cr = statistics.median([pct(r.get("conversion_rate")) or 0 for r in top]) if top else 0
    med_br = statistics.median([pct(r.get("bounce_rate")) or 0 for r in top]) if top else 0

    names = [q for q, r in rows.items() if max(r.get("browse_sessions") or 0, r.get("prev_browse_sessions") or 0) >= a.min_sessions]
    sigs = {q: signature(profiles[q], set(a.ignore)) for q in names if q in profiles}

    # Union-find over queries that share enough dominant values.
    parent = {q: q for q in sigs}

    def find(q):
        while parent[q] != q:
            parent[q] = parent[parent[q]]
            q = parent[q]
        return q

    keys = list(sigs)
    for i, x in enumerate(keys):
        for y in keys[i + 1:]:
            if len(collapse(sigs[x] & sigs[y])) >= a.min_shared:
                parent[find(x)] = find(y)

    groups = {}
    for q in keys:
        groups.setdefault(find(q), []).append(q)

    themes = []
    for members in groups.values():
        sets = [sigs[q] for q in members]
        shared = set.intersection(*sets) if sets else set()
        common = sorted(v for v in set.union(*sets) if sum(v in s for s in sets) * 2 >= len(sets)) if sets else []
        cur = sum(rows[q].get("browse_sessions") or 0 for q in members)
        prev = sum(rows[q].get("prev_browse_sessions") or 0 for q in members)
        expected = prev * growth
        revenue = sum(money(rows[q].get("revenue")) for q in members)
        cr = sum((pct(rows[q].get("conversion_rate")) or 0) * (rows[q].get("browse_sessions") or 0) for q in members) / cur if cur else None
        br = sum((pct(rows[q].get("bounce_rate")) or 0) * (rows[q].get("browse_sessions") or 0) for q in members) / cur if cur else None
        underserved = []
        for q in members:
            r = rows[q]
            qcr, qbr = pct(r.get("conversion_rate")) or 0, pct(r.get("bounce_rate")) or 0
            if (med_cr and qcr < 0.75 * med_cr) or (med_br and qbr > 1.5 * med_br):
                underserved.append({"query": r["query"], "sessions": r.get("browse_sessions"),
                                    "conversion_rate": r.get("conversion_rate"), "bounce_rate": r.get("bounce_rate")})
        themes.append({
            "queries": sorted(members, key=lambda q: -(rows[q].get("browse_sessions") or 0)),
            "shared_by_all": sorted(shared),
            "shared_by_most": common,
            "sessions": cur,
            "prev_sessions": prev,
            "vs_baseline_pct": round((cur / expected - 1) * 100, 1) if expected else None,
            "revenue": round(revenue, 2),
            "conversion_rate": round(cr, 2) if cr is not None else None,
            "bounce_rate": round(br, 2) if br is not None else None,
            "underserved": underserved,
        })
    themes.sort(key=lambda t: -t["sessions"])

    json.dump({
        "baseline_change_pct": a.baseline,
        "top20_median_conversion": med_cr,
        "top20_median_bounce": med_br,
        "themes": themes,
        "unprofiled": sorted((q for q in names if q not in profiles), key=lambda q: -(rows[q].get("browse_sessions") or 0))[:30],
    }, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
