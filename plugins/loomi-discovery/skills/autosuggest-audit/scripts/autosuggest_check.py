#!/usr/bin/env python3
"""Check collected autosuggest results against query performance.

Usage:
  python3 autosuggest_check.py suggestions.json [queries.json ...]

suggestions.json maps each prefix you tested to the list that
`get_autosuggest_results` returned for it, for example:

  {"ts": ["tshirt", "camo tshirt"], "sc": ["scharf", "scarf"], "coc": []}

Each queries.json is a saved `get_discovery_query_performance` response
(the tool envelope, its `data` object, or a plain list of rows). Pass the
top_searched page, a revenue-sorted page and any `search=` pages you pulled.
Rows are merged by query text.

It prints one JSON object with:
  missing_top_queries   queries with traffic that never appear, even though
                        a prefix of them was tested (e.g. "cocktail dress"
                        absent from "co" and "coc")
  untested_top_queries  queries with traffic whose prefixes you didn't test
  near_duplicates       suggestions that differ only by spacing, hyphens,
                        apostrophes, plural "s" or men/mens
                        ("men jeans", "mens jeans"), with metrics if known
  modifier_suggestions  "<product> <attribute>" suggestions such as
                        "skirt colors" or "dress fabric", with their revenue
                        per visit next to the bare product query's
  slot_hogs             prefixes where one lead word that isn't itself a
                        suggestion fills 5 or more slots (e.g. "disney ..."
                        x10 under "di", "sweet dreams ..." x9 under "sw")
  weaker_wording        suggestions whose metrics are well below a close
                        variant that isn't suggested

Treat every flag as a lead to check, not a verdict. Standard library only;
no network access.
"""
import json
import re
import sys
from collections import defaultdict

MODIFIERS = {
    "color", "colors", "colour", "colours", "style", "styles", "fabric", "fabrics",
    "trend", "trends", "length", "lengths", "size", "sizes", "material", "materials",
    "brand", "brands", "shape", "cut", "type", "types", "ideas", "guide",
}
HOG_MIN = 5
WEAK_RATIO = 0.75  # flag when revenue per visit is under 75% of the variant's


def money(value):
    if value in (None, "", "N/A"):
        return None
    try:
        return float(str(value).replace("$", "").replace(",", ""))
    except ValueError:
        return None


def pct(value):
    if value in (None, "", "N/A"):
        return None
    try:
        return float(str(value).rstrip("%"))
    except ValueError:
        return None


def load_rows(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("result"), dict):
        data = data["result"]
    if isinstance(data, dict):
        data = data.get("data", data)
    if isinstance(data, dict):
        data = data.get("rows", [])
    return data if isinstance(data, list) else []


def key(text):
    t = text.lower().strip()
    t = re.sub(r"\bmen'?s\b", "men", t)
    t = re.sub(r"\bwomen'?s\b", "women", t)
    t = re.sub(r"[^a-z0-9 ]", "", t)
    words = [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in t.split()]
    return "".join(words)


def metrics(row):
    if not row:
        return None
    return {
        "sessions": row.get("browse_sessions") or row.get("visits"),
        "conversion_rate": pct(row.get("conversion_rate")),
        "rpv": money(row.get("rpv")),
        "revenue": money(row.get("revenue")),
    }


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    with open(argv[0], encoding="utf-8") as f:
        suggestions = json.load(f)
    rows = {}
    for path in argv[1:]:
        for row in load_rows(path):
            q = str(row.get("query", "")).strip().lower()
            if q and q not in rows:
                rows[q] = row

    shown = {}
    for prefix, items in suggestions.items():
        for pos, s in enumerate(items or []):
            shown.setdefault(s.lower(), []).append(f"{prefix}#{pos + 1}")
    prefixes = [p.lower() for p in suggestions]

    shown_keys = {}
    for s in shown:
        shown_keys.setdefault(key(s), s)
    missing, untested = [], []
    traffic = sorted(rows.items(), key=lambda kv: -(kv[1].get("browse_sessions") or 0))
    for q, row in traffic:
        if (row.get("browse_sessions") or 0) == 0 or q in shown:
            continue
        if key(q) in shown_keys:
            continue  # a near-duplicate wording is suggested; see near_duplicates
        tested = [p for p in prefixes if q.startswith(p)]
        entry = {"query": q, **metrics(row)}
        if tested:
            entry["tested_prefixes"] = tested
            missing.append(entry)
        else:
            untested.append(q)

    groups = defaultdict(set)
    for s in shown:
        groups[key(s)].add(s)
    for q in rows:
        if key(q) in groups:
            groups[key(q)].add(q)
    near_dupes = []
    for members in groups.values():
        suggested = [m for m in members if m in shown]
        if len(members) > 1 and suggested:
            near_dupes.append({
                m: {"suggested_at": shown.get(m, []), "metrics": metrics(rows.get(m))}
                for m in sorted(members)
            })

    modifiers = []
    for s in shown:
        words = s.split()
        if len(words) >= 2 and words[-1] in MODIFIERS:
            base = " ".join(words[:-1])
            modifiers.append({
                "suggestion": s,
                "suggested_at": shown[s],
                "metrics": metrics(rows.get(s)),
                "base_query": base,
                "base_metrics": metrics(rows.get(base)),
            })

    hogs = []
    for prefix, items in suggestions.items():
        items = [s.lower() for s in items or []]
        lead = defaultdict(list)
        for s in items:
            words = s.split()
            if len(words) >= 2:
                lead[words[0]].append(s)
        for word, members in lead.items():
            # A lead word that is itself a suggestion ("skirt", "jersey") is a
            # product family, not a hog; a brand or theme ("disney") is.
            if len(members) >= HOG_MIN and word not in items:
                hogs.append({"prefix": prefix, "lead_word": word, "slots": len(members),
                             "of": len(items), "examples": members[:3]})

    weaker = []
    for members in groups.values():
        scored = [(m, metrics(rows.get(m))) for m in members if rows.get(m)]
        scored = [(m, x) for m, x in scored if x and x["rpv"] is not None and (x["sessions"] or 0) > 0]
        if len(scored) < 2:
            continue
        best = max(scored, key=lambda mx: mx[1]["rpv"])
        for m, x in scored:
            if m in shown and m != best[0] and best[1]["rpv"] and x["rpv"] < WEAK_RATIO * best[1]["rpv"]:
                weaker.append({"suggested": m, "metrics": x, "better_variant": best[0],
                               "better_metrics": best[1], "better_is_suggested": best[0] in shown})

    print(json.dumps({
        "prefixes_tested": len(suggestions),
        "distinct_suggestions": len(shown),
        "missing_top_queries": missing,
        "untested_top_queries": untested[:20],
        "near_duplicates": near_dupes,
        "modifier_suggestions": sorted(modifiers, key=lambda m: -((m["metrics"] or {}).get("sessions") or 0)),
        "slot_hogs": hogs,
        "weaker_wording": weaker,
    }, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
