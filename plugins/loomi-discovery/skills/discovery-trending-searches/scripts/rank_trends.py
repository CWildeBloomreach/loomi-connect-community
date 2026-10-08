#!/usr/bin/env python3
"""Rank trending search queries from Loomi Connect `get_discovery_query_performance` output.

Usage:
  python3 rank_trends.py --baseline -2.86 [--min-sessions 30] [--top 15] page1.json [page2.json ...]

Each input file is the raw JSON returned by get_discovery_query_performance (current period
with prev_* columns). --baseline is the overall search browse_sessions % change for the same
window, from get_discovery_search_performance, so trends are measured against site-wide growth.
Prints JSON with rising, new and falling queries. Standard library only; no network access.
"""
import argparse
import json
import math
import sys


def money(v):
    return float(v.replace("$", "").replace(",", "")) if isinstance(v, str) else float(v or 0)


def load_rows(paths):
    rows = {}
    for path in paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for r in (data.get("data") or data).get("rows", []):
            rows[r["query"].strip().lower()] = r
    return list(rows.values())


def score(rows, baseline_pct, min_sessions):
    growth = 1 + baseline_pct / 100
    rising, new, falling = [], [], []
    for r in rows:
        cur, prev = r.get("browse_sessions") or 0, r.get("prev_browse_sessions") or 0
        if max(cur, prev) < min_sessions:
            continue
        expected = prev * growth
        item = {
            "query": r["query"],
            "sessions": cur,
            "prev_sessions": prev,
            "change_pct": round((cur / prev - 1) * 100, 1) if prev else None,
            "vs_baseline_pct": round((cur / expected - 1) * 100, 1) if expected else None,
            "extra_sessions": round(cur - expected),
            "revenue": money(r.get("revenue")),
            "conversion_rate": r.get("conversion_rate"),
            "bounce_rate": r.get("bounce_rate"),
        }
        # Lift weighted by volume, so a big query growing 30% outranks a tiny one growing 200%.
        item["trend_score"] = round(item["extra_sessions"] / math.sqrt(max(expected, 1)), 2)
        if prev == 0:
            new.append(item)
        elif item["extra_sessions"] > 0:
            rising.append(item)
        else:
            falling.append(item)
    rising.sort(key=lambda i: i["trend_score"], reverse=True)
    falling.sort(key=lambda i: i["trend_score"])
    new.sort(key=lambda i: i["sessions"], reverse=True)
    return rising, new, falling


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--baseline", type=float, required=True, help="site search sessions %% change")
    ap.add_argument("--min-sessions", type=int, default=30)
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    rows = load_rows(a.files)
    rising, new, falling = score(rows, a.baseline, a.min_sessions)
    json.dump({
        "queries_considered": len(rows),
        "baseline_change_pct": a.baseline,
        "rising": rising[:a.top],
        "new": new[:a.top],
        "falling": falling[:a.top],
    }, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
