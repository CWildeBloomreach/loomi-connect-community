#!/usr/bin/env python3
"""Classify new arrivals in a Bloomreach Discovery account and compare them with the rest of the catalog.

Usage:
  python3 new_arrivals.py products.json [more.json ...] --new new_p*.json [options]
  python3 new_arrivals.py products.json --fallback-no-prev [options]

products.json is the raw JSON from get_discovery_product_performance_table for the window being
judged (all pages; any sort). The product table has no release date and leaves out products with
no views in either period, so new arrivals are supplied separately.

Options:
  --new FILE [FILE ...]   the new-arrival list: saved product grid pages (query "*", an fq on the
                          release attribute, fl including pid and ideally days_since_release), or
                          text files with one "pid" or "pid,days_since_release" per line.
  --fallback-no-prev      no release data: treat products with views now and none in the previous
                          period as new. Say so in the output.
  --days N                the report window in days (default 30). Products released N or fewer
                          days ago are judged on the days they have been live.
  --lag N                 days between the report's last day and today (default 2). A product
                          released fewer than N days ago has no report data yet: too early.
  --no-age                judge every product on the whole window (ignore release age). Applied
                          automatically when the release data check fails.
  --positions FILE        optional JSON from the rank checks: {"<pid>": {"where": "jeans",
                          "position": 31}, ...}. A null position means not in the rows fetched.
  --min-visits N          fewer visits than this is too early to judge rates (default 30)
  --gap F                 how far from the median counts as well below/above (default 0.15)
  --seen F                exposure index at or above this counts as "seen" (default 0.5)
  --invisible F           exposure index below this counts as invisible (default 0.1)
  --fold N                a rank deeper than this is "off the first page" (default 24)
  --limit N               rows per group in the output (default 15)
  --markdown              print Markdown instead of JSON

Exposure index = the product's visits per day live / the median catalog product's visits per day.
Rates are judged against the median catalog product with at least --min-visits visits; "well
below/above" also needs the product's 90% Wilson interval to exclude the median.

Groups (each new product appears once, checked in this order):
  invisible     no visits, missing from the report, or exposure index below --invisible
  too_early     fewer than --min-visits visits; rates can't be judged yet
  slow_start    seen (exposure >= --seen) but ATC or conversion well below typical
  buried        conversion well above typical but exposure below 1 (or ranked off the first
                page in --positions)
  breakout      exposure >= 1, conversion not below typical, and either conversion well above
                typical or revenue per day in the catalog's top 10%
  on_track      everything else

Revenue at stake (an upper bound for the period, not a forecast):
  buried      (median visits/day x days live - visits) x CR halfway to the median x AOV
  slow_start  visits x (median CR - CR) x AOV
Also checks the release data against traffic: a product released inside the window should have no
views in the previous period. If most "new" products do, the release attribute is unreliable.
Standard library only; no network access.
"""
import argparse
import json
import math
import statistics
import sys

Z = 1.645  # 90% two-sided


def num(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("$", "").replace(",", "").replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def unwrap(data):
    if isinstance(data, dict) and isinstance(data.get("result"), dict):
        data = data["result"]
    return data.get("data", data) if isinstance(data, dict) else data


def wilson(successes, n):
    if n <= 0:
        return 0.0, 1.0
    p = successes / n
    d = 1 + Z * Z / n
    c = p + Z * Z / (2 * n)
    m = Z * math.sqrt(max(p * (1 - p) / n + Z * Z / (4 * n * n), 0))
    return (c - m) / d, (c + m) / d


def pct(values, p):
    v = sorted(values)
    if not v:
        return 0
    k = (len(v) - 1) * p / 100
    lo, hi = math.floor(k), math.ceil(k)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def load_new(paths):
    """Return {pid: days_since_release or None}."""
    out = {}
    for path in paths:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        try:
            data = unwrap(json.loads(text))
            for d in data.get("response", {}).get("docs", []):
                if d.get("pid") is None:
                    continue
                days = num(d.get("days_since_release"))
                out[str(d["pid"])] = days
        except (ValueError, AttributeError):
            for line in text.splitlines():
                parts = [p.strip() for p in line.split(",")]
                if parts and parts[0]:
                    out[parts[0]] = num(parts[1]) if len(parts) > 1 else None
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("products", nargs="+")
    ap.add_argument("--new", nargs="+", default=[])
    ap.add_argument("--fallback-no-prev", action="store_true")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--lag", type=int, default=2)
    ap.add_argument("--no-age", action="store_true")
    ap.add_argument("--positions")
    ap.add_argument("--min-visits", type=int, default=30)
    ap.add_argument("--gap", type=float, default=0.15)
    ap.add_argument("--seen", type=float, default=0.5)
    ap.add_argument("--invisible", type=float, default=0.1)
    ap.add_argument("--fold", type=int, default=24)
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    if not a.new and not a.fallback_no_prev:
        ap.error("pass --new with the new-arrival list, or --fallback-no-prev")

    rows, seen_pids = [], set()
    for p in a.products:
        with open(p, encoding="utf-8") as f:
            for r in unwrap(json.load(f)).get("rows", []):
                pid = str(r.get("prod_id"))
                if pid in seen_pids:
                    continue
                seen_pids.add(pid)
                rows.append({
                    "pid": pid, "title": r.get("product_title"), "brand": (r.get("brand") or "").strip() or "(none)",
                    "visits": num(r.get("visits")) or 0, "prev_visits": num(r.get("prev_visits")) or 0,
                    "atc": num(r.get("atc")) or 0, "conversions": num(r.get("conversions")) or 0,
                    "revenue": num(r.get("revenue")) or 0, "prev_revenue": num(r.get("prev_revenue")) or 0,
                    "aov": num(r.get("aov")) or 0,
                })
    by_pid = {r["pid"]: r for r in rows}

    if a.fallback_no_prev:
        new = {r["pid"]: None for r in rows if r["visits"] > 0 and r["prev_visits"] == 0}
        source = "fallback: views this period and none in the previous period"
    else:
        new = load_new(a.new)
        source = "release attribute"
    positions = {}
    if a.positions:
        with open(a.positions, encoding="utf-8") as f:
            positions = {str(k): v for k, v in json.load(f).items()}

    days = a.days
    # Release-data sanity check: a product released inside the window can't have had views in the
    # previous period.
    judged_release = [by_pid[p] for p, d in new.items() if p in by_pid and (d is not None or a.fallback_no_prev)]
    conflicts = [r for r in judged_release if r["prev_visits"] > 0]
    share = len(conflicts) / len(judged_release) if judged_release else None
    check = {"new_with_release_age": len(judged_release), "with_previous_period_views": len(conflicts),
             "share": round(share, 4) if share is not None else None}
    use_age = not a.no_age and share is not None and share <= 0.5 and not a.fallback_no_prev
    if share is not None and share > 0.5:
        check["verdict"] = ("UNRELIABLE: most products released inside the window already had views in the "
                            "previous period, so the release attribute doesn't match traffic. Release ages were "
                            "ignored (every product judged on the whole window). Treat the list of new products "
                            "with caution and fix the feed.")
    elif share is not None and share > 0.1:
        check["verdict"] = "PARTLY RELIABLE: some 'new' products had earlier views (relaunches, pre-orders or feed errors)."
    elif share is not None:
        check["verdict"] = "OK: new products had no earlier views."
    elif a.fallback_no_prev:
        check["verdict"] = ("Fallback used: no release data. " + (
            "No product had views this period and none in the previous one, so nothing looks new."
            if not new else "New = views this period, none in the previous period."))
    else:
        check["verdict"] = "Not checked: no release age per product. Every product judged on the whole window."
    check["age_adjusted"] = use_age

    for r in rows:
        v = r["visits"]
        r["atc_rate"] = r["atc"] / v if v else 0
        r["cr"] = r["conversions"] / v if v else 0
        r["rpv"] = r["revenue"] / v if v else 0
        r["days_live"] = days
        r["is_new"] = r["pid"] in new
        r["no_data_yet"] = False
        if r["is_new"] and use_age and new.get(r["pid"]) is not None:
            live = int(new[r["pid"]]) + 1 - a.lag
            r["no_data_yet"] = live < 1
            r["days_live"] = max(1, min(days, live))
        r["daily"] = v / r["days_live"]
        r["rev_daily"] = r["revenue"] / r["days_live"]

    # Baselines from established products (not new), falling back to everything.
    est = [r for r in rows if not r["is_new"] and r["visits"] >= a.min_visits] or \
          [r for r in rows if r["visits"] >= a.min_visits]
    med_daily = statistics.median([r["daily"] for r in est]) if est else 0
    med_atc = statistics.median([r["atc_rate"] for r in est]) if est else 0
    med_cr = statistics.median([r["cr"] for r in est]) if est else 0
    med_rpv = statistics.median([r["rpv"] for r in est]) if est else 0
    top_rev_daily = pct([r["rev_daily"] for r in est], 90)
    lo_gap, hi_gap = 1 - a.gap, 1 + a.gap

    def aov(r):
        return r["aov"] or (r["revenue"] / r["conversions"] if r["conversions"] else 0)

    groups = {g: [] for g in ("invisible", "too_early", "slow_start", "buried", "breakout", "on_track")}
    for pid, dsr in new.items():
        r = by_pid.get(pid)
        if r is None:
            if use_age and dsr is not None and int(dsr) + 1 - a.lag < 1:
                groups["too_early"].append({"pid": pid, "title": None, "brand": None, "visits": 0, "days_live": 0,
                                            "reason": "released after the report's last day"})
                continue
            groups["invisible"].append({"pid": pid, "title": None, "brand": None, "visits": 0,
                                        "days_live": None,
                                        "reason": "not in the product report: no views this period or last"})
            continue
        v = r["visits"]
        expo = r["daily"] / med_daily if med_daily else 0
        pos = positions.get(pid) or {}
        off_page = bool(pos) and (pos.get("position") is None or pos.get("position") > a.fold)
        item = {
            "pid": pid, "title": r["title"], "brand": r["brand"], "days_live": r["days_live"],
            "visits": int(v), "prev_visits": int(r["prev_visits"]), "exposure_index": round(expo, 2),
            "atc_rate": round(r["atc_rate"], 4), "conversion_rate": round(r["cr"], 4),
            "rpv": round(r["rpv"], 2), "aov": round(aov(r), 2), "revenue": round(r["revenue"], 2),
            "rank_check": pos or None,
        }
        if r["no_data_yet"]:
            item["reason"] = "released after the report's last day"
            groups["too_early"].append(item)
            continue
        if v == 0 or expo < a.invisible:
            item["reason"] = "no views this period" if v == 0 else f"exposure index {expo:.2f}"
            groups["invisible"].append(item)
            continue
        if v < a.min_visits:
            groups["too_early"].append(item)
            continue
        atc_lo, atc_hi = wilson(r["atc"], v)
        cr_lo, cr_hi = wilson(r["conversions"], v)
        atc_low = r["atc_rate"] <= lo_gap * med_atc and atc_hi < med_atc
        cr_low = r["cr"] <= lo_gap * med_cr and cr_hi < med_cr
        cr_high = r["cr"] >= hi_gap * med_cr and cr_lo > med_cr
        if expo >= a.seen and (atc_low or cr_low):
            stake = v * max(med_cr - r["cr"], 0) * aov(r)
            item.update(revenue_at_stake=round(stake, 2),
                        working=f"{v:.0f} visits x ({med_cr:.1%} - {r['cr']:.1%}) CR x ${aov(r):,.2f}",
                        weak="add-to-cart" if atc_low else "checkout (ATC normal, conversion low)")
            groups["slow_start"].append(item)
        elif cr_high and (expo < 1 or off_page):
            target = med_daily * r["days_live"]
            blended = (r["cr"] + med_cr) / 2
            stake = max(target - v, 0) * blended * aov(r)
            item.update(revenue_at_stake=round(stake, 2),
                        working=f"({target:.0f} - {v:.0f}) visits x {blended:.1%} CR (halfway to median) x ${aov(r):,.2f}")
            groups["buried"].append(item)
        elif expo >= 1 and not cr_low and (cr_high or r["rev_daily"] >= top_rev_daily):
            item["revenue_per_day"] = round(r["rev_daily"], 2)
            item["orders_per_day"] = round(r["conversions"] / r["days_live"], 2)
            groups["breakout"].append(item)
        else:
            groups["on_track"].append(item)

    order = {"invisible": lambda i: i["visits"], "too_early": lambda i: -i["visits"],
             "slow_start": lambda i: -i.get("revenue_at_stake", 0), "buried": lambda i: -i.get("revenue_at_stake", 0),
             "breakout": lambda i: -i.get("revenue_per_day", 0), "on_track": lambda i: -i["revenue"]}
    out_groups = {}
    for g, items in groups.items():
        items.sort(key=order[g])
        out_groups[g] = {"count": len(items),
                         "revenue_at_stake": round(sum(i.get("revenue_at_stake", 0) for i in items), 2),
                         "products": items[: a.limit]}

    # Group comparison: new arrivals vs the rest.
    def summary(sel):
        n = len(sel)
        vis = sum(r["visits"] for r in sel)
        pv = sum(r["prev_visits"] for r in sel)
        rev = sum(r["revenue"] for r in sel)
        atc = sum(r["atc"] for r in sel)
        conv = sum(r["conversions"] for r in sel)
        return {"products": n, "visits": vis, "prev_visits": pv, "revenue": round(rev, 2),
                "atc_rate": round(atc / vis, 4) if vis else 0, "conversion_rate": round(conv / vis, 4) if vis else 0,
                "rpv": round(rev / vis, 2) if vis else 0}
    new_rows = [r for r in rows if r["is_new"]]
    rest_rows = [r for r in rows if not r["is_new"]]
    s_new, s_rest = summary(new_rows), summary(rest_rows)
    missing_new = sum(1 for p in new if p not in by_pid)
    n_products = len(rows) + missing_new
    tot_v = s_new["visits"] + s_rest["visits"]
    tot_pv = s_new["prev_visits"] + s_rest["prev_visits"]
    tot_r = s_new["revenue"] + s_rest["revenue"]
    prod_share = (len(new)) / n_products if n_products else 0
    view_share = s_new["visits"] / tot_v if tot_v else 0
    avg_days_live = statistics.mean([r["days_live"] for r in new_rows]) if new_rows else days
    comparison = {
        "new": s_new, "rest": s_rest, "new_not_in_report": missing_new,
        "product_share": round(prod_share, 4), "view_share": round(view_share, 4),
        "revenue_share": round(s_new["revenue"] / tot_r, 4) if tot_r else 0,
        "prev_view_share": round(s_new["prev_visits"] / tot_pv, 4) if tot_pv else 0,
        "visibility_index": round(view_share / prod_share, 2) if prod_share else None,
        "average_days_live": round(avg_days_live, 1),
        "age_adjusted_visibility_index": round((view_share / prod_share) / (avg_days_live / days), 2)
        if prod_share and avg_days_live and use_age else None,
    }

    out = {
        "source": source, "window_days": days, "new_products": len(new),
        "baselines": {"median_visits_per_day": round(med_daily, 2), "median_atc_rate": round(med_atc, 4),
                      "median_conversion_rate": round(med_cr, 4), "median_rpv": round(med_rpv, 2),
                      "top10_revenue_per_day": round(top_rev_daily, 2),
                      "judged_on": "established products (not new) with at least --min-visits visits"},
        "release_data_check": check, "comparison": comparison, "groups": out_groups,
    }
    if a.markdown:
        print_markdown(out)
    else:
        json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
        print()


def print_markdown(out):
    b, c, chk = out["baselines"], out["comparison"], out["release_data_check"]
    print(f"New arrivals: {out['new_products']} ({out['source']}), window {out['window_days']} days")
    print(f"Release data check: {chk['with_previous_period_views']} of {chk['new_with_release_age']} "
          f"had previous-period views. {chk['verdict']}\n")
    print(f"Typical established product: {b['median_visits_per_day']} visits/day, ATC {b['median_atc_rate']:.1%}, "
          f"CR {b['median_conversion_rate']:.1%}, RPV ${b['median_rpv']:.2f}\n")
    print("| | Products | Visits | Revenue | ATC | CR | RPV |")
    print("|---|---|---|---|---|---|---|")
    for k in ("new", "rest"):
        s = c[k]
        print(f"| {k} | {s['products']:,} | {s['visits']:,.0f} | ${s['revenue']:,.0f} | {s['atc_rate']:.1%} | "
              f"{s['conversion_rate']:.1%} | ${s['rpv']:.2f} |")
    print(f"\nShare of products {c['product_share']:.1%}; share of views {c['view_share']:.1%} "
          f"(previous period {c['prev_view_share']:.1%}); share of revenue {c['revenue_share']:.1%}. "
          f"Visibility index {c['visibility_index']} (age-adjusted {c['age_adjusted_visibility_index']}, "
          f"average {c['average_days_live']} days live).\n")
    titles = {"breakout": "Breakout", "buried": "Buried", "slow_start": "Slow start",
              "invisible": "Invisible", "too_early": "Too early to judge", "on_track": "On track"}
    for g, t in titles.items():
        grp = out["groups"][g]
        extra = f", up to ${grp['revenue_at_stake']:,.0f} at stake" if grp["revenue_at_stake"] else ""
        print(f"### {t}: {grp['count']}{extra}\n")
        if not grp["products"] or g == "on_track":
            print("None.\n" if not grp["products"] else "")
            continue
        print("| PID | Title | Brand | Days live | Visits | Exposure | ATC | CR | Revenue | Note |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for i in grp["products"]:
            note = i.get("working") or i.get("reason") or (
                f"${i['revenue_per_day']:,.0f}/day, {i['orders_per_day']} orders/day" if "revenue_per_day" in i else "")
            rc = i.get("rank_check")
            if rc:
                where = rc.get("where", "?")
                pos = rc.get("position")
                note += f"; {where}: " + (f"position {pos}" if pos else "not in the rows fetched")
            print(f"| {i['pid']} | {(i.get('title') or '')[:45]} | {i.get('brand') or ''} | {i.get('days_live')} | "
                  f"{i['visits']:,} | {i.get('exposure_index', '')} | {i.get('atc_rate', 0):.1%} | "
                  f"{i.get('conversion_rate', 0):.1%} | ${i.get('revenue', 0):,.0f} | {note} |")
        print()


if __name__ == "__main__":
    main()
