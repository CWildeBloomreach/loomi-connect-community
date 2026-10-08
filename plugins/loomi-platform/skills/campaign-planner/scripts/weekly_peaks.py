#!/usr/bin/env python3
"""Roll daily figures into weeks and find the peak weeks.

Standard library only. No network access. Prints Markdown, or JSON with --json.

Accepts either of these, saved to a file by the assistant:

1. An Engagement EQL response for a daily breakdown, e.g.
     select count event purchase by event purchase timestamp grouping top 60
       format year month day since <start>Z until <end>Z
   Rows look like {"headers": [{"value": <unix seconds>}], "values": [n]}.
   The whole tool response, or just its "data" object, is fine.

2. A Discovery get_discovery_trend response. Rows look like
   {"cdate": "20251128", "revenue": "$1,149,791.88"}. Use --series previous
   to read the comparison series instead of the current one.

Usage:
  python3 weekly_peaks.py purchases.json [--week-start mon] [--label "Purchases"]
  python3 weekly_peaks.py trend.json --metric revenue
  python3 weekly_peaks.py purchases.json --moments moments.json

--moments takes the JSON output of retail_dates.py (--json) and tags each week
with the moments that fall in it.

Engagement day buckets are in the project's reporting timezone, so their
timestamps can sit an hour or two either side of UTC midnight (and shift at
daylight saving). This script rounds each bucket to the nearest calendar date
before grouping, which handles that.

A week's "index" is its total divided by the median week in the input
(1.00 = a typical week). Partial weeks at either end are flagged, and are
not used for the median.
"""

import argparse
import json
import statistics
import sys
from datetime import date, datetime, timedelta, timezone

WEEKDAYS = {"mon": 0, "sun": 6, "sat": 5}


def to_number(v):
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return 0.0
    s = str(v).replace("$", "").replace(",", "").replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


def nearest_date(ts):
    dt = datetime.fromtimestamp(int(ts), tz=timezone.utc) + timedelta(hours=12)
    return dt.date()


def parse(data, metric, series):
    if isinstance(data, dict) and "result" in data and isinstance(data["result"], dict):
        data = data["result"]
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
        data = data["data"]
    daily = {}
    if isinstance(data, dict) and "rows" in data:
        for row in data["rows"]:
            h = row.get("headers") or [{}]
            v = h[0].get("value")
            if v is None or h[0].get("type") == "other":
                continue
            d = nearest_date(v)
            daily[d] = daily.get(d, 0.0) + to_number((row.get("values") or [0])[0])
        return daily, "EQL"
    if isinstance(data, dict) and series in data:
        for row in data[series]:
            d = datetime.strptime(str(row["cdate"]), "%Y%m%d").date()
            key = metric or next(k for k in row if k != "cdate")
            daily[d] = daily.get(d, 0.0) + to_number(row.get(key))
        return daily, "Discovery trend"
    raise SystemExit("Unrecognised input: expected EQL 'rows' or a Discovery trend 'current' series.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file")
    p.add_argument("--week-start", default="mon", choices=sorted(WEEKDAYS))
    p.add_argument("--metric", help="Discovery trend metric key (default: the first non-date key)")
    p.add_argument("--series", default="current", choices=["current", "previous"])
    p.add_argument("--label", default="Value")
    p.add_argument("--moments", help="retail_dates.py --json output, to tag weeks")
    p.add_argument("--top", type=int, default=3, help="how many peak weeks to name")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    with open(a.file) as fh:
        daily, source = parse(json.load(fh), a.metric, a.series)
    if not daily:
        print("No data in the window (empty rows). Treat last year's evidence as unavailable.")
        return

    first, last = min(daily), max(daily)
    ws = WEEKDAYS[a.week_start]
    weeks = {}
    for d, v in daily.items():
        start = d - timedelta((d.weekday() - ws) % 7)
        w = weeks.setdefault(start, {"total": 0.0, "days": 0, "peak_day": None, "peak": -1})
        w["total"] += v
        w["days"] += 1
        if v > w["peak"]:
            w["peak"], w["peak_day"] = v, d

    moments = []
    if a.moments:
        with open(a.moments) as fh:
            moments = [m for m in json.load(fh).get("moments", []) if m.get("date")]

    full = [w["total"] for w in weeks.values() if w["days"] == 7] or [w["total"] for w in weeks.values()]
    median = statistics.median(full) if full else 0
    rows = []
    for start in sorted(weeks):
        w = weeks[start]
        end = start + timedelta(6)
        tags = [m["name"] for m in moments if start.isoformat() <= m["date"] <= end.isoformat()]
        rows.append({
            "week_start": start.isoformat(),
            "total": round(w["total"], 2),
            "days": w["days"],
            "partial": w["days"] < 7,
            "index": round(w["total"] / median, 2) if median else None,
            "peak_day": w["peak_day"].isoformat(),
            "moments": tags,
        })
    peaks = sorted((r for r in rows if not r["partial"]), key=lambda r: r["total"], reverse=True)[: a.top]

    if a.json:
        print(json.dumps({"source": source, "first_day": first.isoformat(), "last_day": last.isoformat(),
                          "median_week": median, "weeks": rows, "peaks": [r["week_start"] for r in peaks]}, indent=2))
        return

    print(f"**{a.label} by week** ({source}, {first} to {last}; median full week = {median:,.0f})\n")
    print(f"| Week starting | {a.label} | Index | Peak day | Moments that week |")
    print("|---|---|---|---|---|")
    for r in rows:
        flag = " (partial)" if r["partial"] else ""
        idx = "-" if r["index"] is None else f"{r['index']:.2f}"
        print(f"| {r['week_start']}{flag} | {r['total']:,.0f} | {idx} | {r['peak_day']} | {', '.join(r['moments']) or '-'} |")
    if peaks:
        print("\n**Peak weeks:** " + "; ".join(f"{r['week_start']} (index {r['index']:.2f})" for r in peaks))


if __name__ == "__main__":
    sys.exit(main())
