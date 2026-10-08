#!/usr/bin/env python3
"""Turn Bloomreach Engagement funnel counts into leaks with revenue at stake.

Usage:
    python3 funnel_leaks.py funnel.json [--format markdown|json]

funnel.json (only "steps", "counts" and "aov" are required):
{
  "window": "last 30 days", "conversion_window": "7 days",
  "steps": ["Viewed a product", "Added to cart", "Purchased"],
  "counts": [28500, 4100, 1150],          # data.total.counts from the overall funnel
  "times": [-1, 420.5, 9800.0],           # optional: data.total.times (seconds)
  "aov": 82.0,                            # average order value
  "avg_cart_value": 95.0,                 # optional
  "purchasers_in_window": 1300,           # optional: one-step purchase funnel, for the identity check
  "recovery_rates": [null, 0.01, 0.05],   # optional, per step; defaults: 1% into cart, 5% into purchase
  "segments": {                           # optional: one funnel per value, same steps
    "device = iPhone": [9000, 900, 180],
    "device = Other": [19000, 3150, 960]
  },
  "min_customers": 100                    # optional: below this, no value is given
}

Formulas are in references/revenue-at-stake.md. All values are estimates:
"walking away" is an upper bound; "recoverable" rests on the recovery rate.
Standard library only; no network access.
"""
import argparse
import json
import sys


def pct(x):
    return "—" if x is None else f"{x * 100:.1f}%"


def money(x):
    if x is None:
        return "—"
    if x >= 1000:
        return f"${x:,.0f}"
    return f"${x:,.2f}"


def default_rate(i, n_steps):
    return 0.05 if i == n_steps - 1 else 0.01


def analyse(d):
    steps, n = d["steps"], [int(c or 0) for c in d["counts"]]
    if len(steps) != len(n) or len(n) < 2:
        raise SystemExit("steps and counts must be lists of the same length (2 or more)")
    aov = float(d["aov"])
    cart = d.get("avg_cart_value")
    rates = d.get("recovery_rates") or []
    min_n = int(d.get("min_customers", 100))
    times = d.get("times") or []
    last = len(n) - 1

    caveats = []
    purchase_ok = True
    buyers = d.get("purchasers_in_window")
    if buyers:
        share = n[last] / buyers if buyers else 0
        if share < 0.5:
            purchase_ok = False
            caveats.append(
                f"Only {share * 100:.0f}% of the {buyers:,} purchasers in the window appear at the funnel's last step. "
                "Purchases are probably not linked to the browsing identity (server-side or imported orders), "
                "so the last step isn't a reliable leak. Check purchase tracking (engagement-tracking-health).")

    rows = []
    for i in range(1, len(n)):
        lost = max(n[i - 1] - n[i], 0)
        conv = n[i] / n[i - 1] if n[i - 1] else None
        into_last = i == last
        downstream = 1.0 if into_last else (n[last] / n[i] if n[i] else 0.0)
        value = min(aov, float(cart)) if (into_last and cart) else aov
        rate = rates[i] if i < len(rates) and rates[i] is not None else default_rate(i, len(n))
        assumed = not (i < len(rates) and rates[i] is not None)
        reliable = purchase_ok or not into_last
        enough = n[i - 1] >= min_n
        walk = lost * downstream * value if (reliable and enough) else None
        if not purchase_ok and i < last:
            walk = None  # downstream conversion depends on the unreliable last step
        rows.append({
            "from": steps[i - 1], "to": steps[i], "customers": n[i], "step_conversion": conv, "lost": lost,
            "value_walking_away": walk, "recovery_rate": rate, "rate_assumed": assumed,
            "recoverable": walk * rate if walk is not None else None,
            "avg_seconds": times[i] if i < len(times) and times[i] not in (None, -1) else None,
            "note": "" if reliable else "purchase step unreliable",
        })
        if not enough:
            rows[-1]["note"] = f"fewer than {min_n} customers"

    overall = n[last] / n[0] if n[0] else 0
    segs = []
    for name, counts in (d.get("segments") or {}).items():
        c = [int(x or 0) for x in counts]
        conv = c[-1] / c[0] if c and c[0] else None
        step_convs = [(c[i] / c[i - 1]) if c[i - 1] else None for i in range(1, len(c))]
        gap = None
        if conv is not None and c[0] >= min_n and purchase_ok and conv < overall:
            gap = c[0] * (overall - conv) * aov
        segs.append({"segment": name, "entered": c[0], "end_to_end": conv, "step_conversions": step_convs,
                     "gap_value": gap})
    segs.sort(key=lambda s: -(s["gap_value"] or 0))

    if not purchase_ok:
        weakest = rows[0] if rows else None
    else:
        weakest = max(rows, key=lambda r: r["recoverable"] or 0) if rows else None
    abandoned = None
    if purchase_ok and len(n) >= 2:
        abandoned = {"customers": n[last - 1] - n[last], "avg_cart_value": cart,
                     "value_in_carts": (n[last - 1] - n[last]) * float(cart) if cart else None}
    return {"window": d.get("window"), "conversion_window": d.get("conversion_window"), "steps": steps,
            "counts": n, "overall_conversion": overall, "aov": aov, "rows": rows, "segments": segs,
            "abandoned_carts": abandoned, "biggest_leak": weakest, "caveats": caveats}


def render(r):
    out = []
    out.append(f"Funnel ({r.get('window') or 'window not given'}, conversion window "
               f"{r.get('conversion_window') or 'not given'}): overall conversion {pct(r['overall_conversion'])}, "
               f"AOV {money(r['aov'])}.\n")
    out.append("| Step | Customers | Step conversion | Lost | Value walking away | Recoverable (rate) | Avg time | Note |")
    out.append("|---|---|---|---|---|---|---|---|")
    out.append(f"| {r['steps'][0]} | {r['counts'][0]:,} | — | | | | | |")
    for row in r["rows"]:
        rate = f"{row['recovery_rate'] * 100:g}%{' assumed' if row['rate_assumed'] else ''}"
        t = f"{row['avg_seconds'] / 3600:.1f} h" if row["avg_seconds"] else ""
        out.append(f"| {row['to']} | {row['customers']:,} | {pct(row['step_conversion'])} | {row['lost']:,} | "
                   f"{money(row['value_walking_away'])} | {money(row['recoverable'])} ({rate}) | {t} | {row['note']} |")
    if r["segments"]:
        out.append("\n| Segment | Entered | End-to-end | Step conversions | Gap vs overall |")
        out.append("|---|---|---|---|---|")
        for s in r["segments"]:
            sc = " → ".join(pct(x) for x in s["step_conversions"])
            out.append(f"| {s['segment']} | {s['entered']:,} | {pct(s['end_to_end'])} | {sc} | {money(s['gap_value'])} |")
    a = r["abandoned_carts"]
    if a:
        out.append(f"\nAbandoned carts: {a['customers']:,} customers"
                   + (f", average cart {money(a['avg_cart_value'])}, about {money(a['value_in_carts'])} left in carts"
                      if a["value_in_carts"] else ""))
    b = r["biggest_leak"]
    if b:
        out.append(f"Biggest leak: {b['from']} → {b['to']} ({b['lost']:,} customers lost"
                   + (f", up to {money(b['value_walking_away'])}; about {money(b['recoverable'])} recoverable)"
                      if b["value_walking_away"] is not None else ")"))
    for c in r["caveats"]:
        out.append(f"Caveat: {c}")
    out.append("Values walking away are upper bounds; recoverable values depend on the recovery rate.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("funnel")
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    a = ap.parse_args()
    with open(a.funnel, encoding="utf-8") as f:
        d = json.load(f)
    r = analyse(d)
    if a.format == "json":
        json.dump(r, sys.stdout, indent=2)
        print()
    else:
        print(render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
