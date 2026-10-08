#!/usr/bin/env python3
"""Find strong products ranked low on a Discovery category page.

Usage:
  python3 buried_products.py --grid grid.json [--fold 48] [--top 24] products1.json [products2.json ...]

--grid is the raw JSON from search_discovery_product_grid_insights with search_by="category",
fl including pid,title,brand,price and a large rows value (about 200).
Each products file is the raw JSON from get_discovery_product_performance_table (sorted by
revenue; one or more pages). That report has no category filter, so products are matched to
the category by product ID.

Prints JSON with:
  - top_window: brand mix and repeated titles in the first --top positions;
  - brands_missing_from_top: brands with many products in the category but none in the top;
  - buried: products ranked below --fold whose revenue per visit or conversion rate is at
    least the median of the matched products in the top window;
  - weak_top: products in the top window with views but conversion well below that median.
Standard library only; no network access.
"""
import argparse
import json
import statistics
import sys
from collections import Counter


def num(v):
    if v is None:
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", required=True)
    ap.add_argument("--fold", type=int, default=48, help="positions above this count as visible (default 48)")
    ap.add_argument("--top", type=int, default=24, help="size of the first screen or page (default 24)")
    ap.add_argument("products", nargs="*")
    a = ap.parse_args()

    with open(a.grid, encoding="utf-8") as f:
        grid = unwrap(json.load(f))
    docs = grid.get("response", {}).get("docs", [])
    num_found = grid.get("response", {}).get("numFound")
    pos = {str(d.get("pid")): i + 1 for i, d in enumerate(docs)}

    top = docs[: a.top]
    brand_top = Counter(d.get("brand") or "(none)" for d in top)
    repeated = {t: n for t, n in Counter(d.get("title") for d in top).items() if n > 1}
    brand_facet = {}
    for fc in grid.get("facet_counts", {}).get("facets", []):
        if fc.get("name") == "brand":
            brand_facet = {v.get("name"): v.get("count") for v in fc.get("value", [])}
    missing = sorted(([b, c] for b, c in brand_facet.items() if c and c >= 10 and b not in brand_top),
                     key=lambda x: -x[1])[:10]

    perf = {}
    for p in a.products:
        with open(p, encoding="utf-8") as f:
            for r in unwrap(json.load(f)).get("rows", []):
                perf[str(r.get("prod_id"))] = r

    matched = []
    for pid, rank in pos.items():
        r = perf.get(pid)
        if not r:
            continue
        visits = num(r.get("visits")) or 0
        matched.append({"rank": rank, "pid": pid, "title": r.get("product_title"), "brand": r.get("brand"),
                        "visits": visits, "revenue": num(r.get("revenue")),
                        "rpv": num(r.get("rpv")), "conversion_rate": num(r.get("conversion_rate"))})
    matched.sort(key=lambda x: x["rank"])
    in_top = [m for m in matched if m["rank"] <= a.top]
    med_rpv = statistics.median([m["rpv"] for m in in_top if m["rpv"] is not None]) if in_top else None
    med_cvr = statistics.median([m["conversion_rate"] for m in in_top if m["conversion_rate"] is not None]) if in_top else None

    buried = [m for m in matched if m["rank"] > a.fold and m["visits"] >= 50 and med_rpv is not None
              and ((m["rpv"] or 0) >= med_rpv or (m["conversion_rate"] or 0) >= (med_cvr or 0))]
    weak_top = [m for m in in_top if m["visits"] >= 50 and med_cvr and (m["conversion_rate"] or 0) < 0.75 * med_cvr]

    json.dump({
        "num_found": num_found, "ranked_rows_checked": len(docs), "products_with_metrics": len(matched),
        "top_window": {"size": a.top, "brands": brand_top.most_common(), "repeated_titles": repeated,
                       "median_rpv": med_rpv, "median_conversion_rate": med_cvr},
        "brands_missing_from_top": missing,
        "buried": buried[:20],
        "weak_top": weak_top,
        "note": "Products without metrics are either new, low-traffic or outside the product report pages you passed.",
    }, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
