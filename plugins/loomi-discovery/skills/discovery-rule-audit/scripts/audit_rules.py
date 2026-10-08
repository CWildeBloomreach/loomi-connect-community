#!/usr/bin/env python3
"""Flag Discovery merchandising rules that need cleaning up.

Reads rule listings you have already saved from Loomi Connect, plus optional
traffic and experiment data, and prints a Markdown cleanup list. It never calls
the network; it only reshapes data the assistant has fetched.

Standard library only.

Usage:
    python3 scripts/audit_rules.py --rules site_ranking.json --rules site_media.json ... \
        [--queries query_perf.json] [--categories category_perf.json] \
        [--experiments experiments.json] [--today 2026-10-08] [--stale-days 90]

Each --rules file is a saved response from one of: list_site_search_ranking_rules,
list_category_ranking_rules, list_ranking_rules_global, list_site_search_media_rules,
list_category_media_rules, list_global_media_rules, list_site_search_facets,
list_category_facets, list_facets_global or search_redirects. Save the whole
response, or just its "data" list. Fetch every page first.

--queries is a saved get_discovery_query_performance response (one big page,
for example page_size=1000). --categories is a saved
get_discovery_category_performance_table response. --experiments is a saved
search_discovery_experiments listing (all statuses).
"""
import argparse
import collections
import datetime as dt
import json
import re
import sys

SEASONAL = re.compile(r"sale|black ?friday|cyber|halloween|christmas|xmas|holiday|summer|winter|spring|autumn|fall|"
                      r"valentine|easter|promo|campaign|launch|demo|test|hackathon|\b20\d\d\b", re.I)
PROTECTED = re.compile(r"do not (delete|change|remove|update)|don'?t (delete|change)", re.I)
SEVERITY = {"high": 0, "medium": 1, "low": 2, "info": 3}


def load(path):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    if isinstance(doc, dict) and "result" in doc and "data" not in doc:
        doc = doc["result"]
    return doc.get("data", doc) if isinstance(doc, dict) else doc


def kind_of(rule):
    rt = {"campaign": "media", "facet": "facet", "redirect": "redirect"}.get(rule.get("ruleType"), rule.get("ruleType") or "rule")
    qts = {q.get("queryType") for q in rule.get("queries") or []}
    scope = "global" if any("global" in (t or "") for t in qts) else ("category" if "category" in qts else "search")
    return f"{scope} {rt}"


def days_since(ms, today):
    if not ms:
        return None
    return (today - dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date()).days


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rules", action="append", required=True)
    ap.add_argument("--queries")
    ap.add_argument("--categories")
    ap.add_argument("--experiments")
    ap.add_argument("--today", help="YYYY-MM-DD (default: today, UTC)")
    ap.add_argument("--stale-days", type=int, default=90, help="disabled this long counts as stale (default 90)")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.timezone.utc).date()
    now_ms = dt.datetime.combine(today, dt.time(), dt.timezone.utc).timestamp() * 1000

    rules, seen = [], set()
    for path in args.rules:
        for r in load(path) or []:
            if r.get("id") not in seen:
                seen.add(r.get("id"))
                rules.append(r)

    query_visits = None
    if args.queries:
        query_visits = {row["query"].strip().lower(): row.get("visits") or 0 for row in load(args.queries)["rows"]}
    cat_visits = None
    if args.categories:
        cat_visits = {str(row.get("cat_id")).strip().lower(): row.get("visits") or 0 for row in load(args.categories)["rows"]}

    exp_rules = collections.defaultdict(list)
    experiments = load(args.experiments) if args.experiments else []
    for e in experiments:
        for b in e.get("buckets") or []:
            info = b.get("ruleIdentifierInfo") or {}
            if info.get("id"):
                exp_rules[info["id"]].append(e)

    findings = []  # (severity, rule_or_None, issue, action)

    def add(sev, rule, issue, action):
        findings.append((sev, rule, issue, action))

    # Per-rule checks.
    for r in rules:
        enabled = bool(r.get("enabled"))
        name = r.get("name") or ""
        expired = r.get("durationTag") == "expired" or (r.get("endedAt") and r["endedAt"] < now_ms)
        protected = bool(PROTECTED.search(name))
        if r.get("isAbTestLive"):
            add("info", r, "In a RUNNING A/B test", "Leave it. It can't be changed or deleted until the test ends.")
            continue
        if expired and enabled:
            add("high", r, "Expired but still switched on", "Disable it, or delete it if the campaign is over.")
        elif expired:
            add("low", r, "Expired and disabled", "Delete it.")
        if not enabled and not expired:
            age = days_since(r.get("lastModifiedAt"), today)
            if r.get("syncStatus") is None:
                add("medium", r, "Disabled and never synced (draft that was never used)", "Delete it, or finish and enable it.")
            elif age is not None and age >= args.stale_days:
                add("low", r, f"Disabled for {age} days", "Delete it if nobody needs it.")
        if enabled and not expired and r.get("durationTag") in (None, "unscheduled") and SEASONAL.search(name):
            add("medium", r, "Never ends, but the name looks seasonal or temporary", "Add an end date, or disable it.")
        if protected:
            add("info", r, f"Named \"{name.strip()}\"", "Don't delete without asking the owner.")
        if r.get("id") in exp_rules:
            statuses = sorted({e.get("experimentStatus") for e in exp_rules[r["id"]]})
            if "DRAFT" in statuses:
                add("medium", r, "Linked to a DRAFT experiment", "Start the experiment or delete the draft.")
            elif enabled and "COMPLETED" in statuses:
                add("info", r, "Was an A/B test variant; still enabled", "Check it was the winner (readout skill).")
        # Traffic. Redirected searches never reach a results page, so they don't show up in
        # query performance; don't judge redirects on it.
        if enabled and not expired and r.get("ruleType") != "redirect":
            for q in r.get("queries") or []:
                text, qt = str(q.get("query", "")).strip().lower(), q.get("queryType")
                if qt == "sitesearch" and query_visits is not None and query_visits.get(text, 0) == 0:
                    add("medium", r, f"No searches for \"{q.get('query')}\" in the period",
                        "Check the match type (phrase-match rules can still fire), then retarget or delete.")
                if qt == "category" and cat_visits is not None and cat_visits.get(text, 0) == 0:
                    add("medium", r, f"No visits to category {q.get('query')} in the period", "Retarget or delete.")

    # Duplicates and overlaps: more than one enabled rule of the same type for the same query.
    groups = collections.defaultdict(list)
    for r in rules:
        if r.get("enabled") and r.get("durationTag") != "expired":
            for q in r.get("queries") or []:
                groups[(r.get("ruleType"), q.get("queryType"), str(q.get("query")).strip().lower())].append(r)
    for (rt, qt, q), rs in sorted(groups.items()):
        if len(rs) > 1:
            ids = ", ".join(str(x["id"]) for x in rs)
            if q == "*":
                issue = f"{len(rs)} enabled global {rt} rules for {qt}"
                action = "Only one un-targeted global rule is allowed per type; check the others' audiences."
            else:
                issue = f"{len(rs)} enabled {rt} rules for \"{q}\" ({qt}): {ids}"
                action = "Fetch each rule: different audiences is fine; same audience means they conflict. Merge them."
            add("medium", None, issue, action)

    # Experiments.
    for e in experiments:
        st = e.get("experimentStatus")
        age = days_since(e.get("modifiedAt"), today)
        if st == "DRAFT" and age is not None and age >= args.stale_days:
            add("low", None, f"Experiment \"{e.get('experimentName')}\" ({e.get('id')}) has been a draft for {age} days",
                "Delete the draft, or check its rules still exist and start it.")
        if st == "RUNNING":
            started = days_since(e.get("startedAt"), today)
            add("info", None, f"Experiment \"{e.get('experimentName')}\" ({e.get('id')}) is RUNNING ({started} days)",
                "Rule changes in its scope are blocked until it ends. Read it out with the readout skill.")
        if st == "COMPLETED" and e.get("startedAt") and e.get("endedAt") and e["endedAt"] - e["startedAt"] < 86_400_000:
            add("low", None, f"Experiment \"{e.get('experimentName')}\" ({e.get('id')}) ran for less than a day",
                "Probably a trial run. Archive it so it doesn't mislead.")

    findings.sort(key=lambda f: (SEVERITY[f[0]], kind_of(f[1]) if f[1] else "", str(f[1].get("id")) if f[1] else ""))
    counts = collections.Counter(kind_of(r) for r in rules)
    enabled = sum(1 for r in rules if r.get("enabled"))
    print(f"Rules checked: {len(rules)} ({enabled} enabled). "
          + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    print(f"Findings: " + ", ".join(f"{s} {n}" for s, n in collections.Counter(f[0] for f in findings).most_common()) + "\n")
    print("| Priority | Rule | Type | Query | Issue | Suggested action |")
    print("|---|---|---|---|---|---|")
    for sev, r, issue, action in findings:
        if r:
            qs = "; ".join(str(q.get("query")) for q in (r.get("queries") or [])[:3])
            label = f"{r.get('id')}" + (f" \"{r['name'].strip()}\"" if r.get("name") else "")
            print(f"| {sev} | {label} | {kind_of(r)} | {qs} | {issue} | {action} |")
        else:
            print(f"| {sev} | — | — | — | {issue} | {action} |")


if __name__ == "__main__":
    sys.exit(main())
