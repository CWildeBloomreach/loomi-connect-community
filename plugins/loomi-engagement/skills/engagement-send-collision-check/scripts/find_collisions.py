#!/usr/bin/env python3
"""Find busy days and possible send collisions in a campaign calendar.

Standard library only. No network access.

Usage:
  python3 find_collisions.py calendar.json [--audiences audiences.json]
         [--utc-offset HOURS] [--same-channel-hours 24] [--cross-channel-hours 4]
         [--busy-day N] [--include-inactive] [--include-webhooks]

calendar.json is the get_campaign_calendar response, either the whole
object ({"success": ..., "campaigns": [...]}) or just the campaigns list.
Several responses (one per week) can be merged into one list first.

audiences.json is optional and maps campaign_id to an audience description
that you worked out from the scenario or campaign definition:

{
  "<campaign_id>": {"segmentation_id": "<id or null>", "segment": "<name or null>",
                     "label": "<short description>", "everyone": false}
}

Rules for comparing two audiences:
  - either is "everyone" (no filter)          -> overlap
  - same segmentation, same segment           -> same audience
  - same segmentation, different segments     -> no overlap (segments are exclusive)
  - anything else, or audience unknown        -> possible overlap
"""

import argparse
import datetime as dt
import json
from collections import defaultdict

INACTIVE = {"draft", "inactive", "finished", "stopped"}


def load_entries(path, include_inactive, include_webhooks):
    data = json.load(open(path))
    if isinstance(data, dict):
        data = data.get("campaigns", [])
    sends = []
    skipped = defaultdict(int)
    for c in data:
        if not include_inactive and str(c.get("status", "")).lower() in INACTIVE:
            skipped[f"{c.get('status')} actions"] += 1
            continue
        channel = c.get("channel") or "unknown"
        if channel == "webhook" and not include_webhooks:
            skipped["webhook actions"] += 1
            continue
        for t in c.get("times") or []:
            start = t.get("start")
            if start is None:
                continue
            sends.append({
                "campaign_id": c.get("campaign_id"),
                "campaign": c.get("campaign_name") or c.get("campaign_id"),
                "action": c.get("action_name") or "",
                "channel": channel,
                "status": c.get("status"),
                "reach": (c.get("results") or {}).get("reach"),
                "ts": int(start),
            })
    # The same action can be listed more than once when windows overlap.
    unique = {(s["campaign_id"], s["action"], s["ts"]): s for s in sends}
    return sorted(unique.values(), key=lambda s: s["ts"]), dict(skipped)


def compare(a, b, audiences):
    if a["campaign_id"] == b["campaign_id"] and a["action"] == b["action"]:
        return None
    aa, ab = audiences.get(a["campaign_id"]), audiences.get(b["campaign_id"])
    if aa is None or ab is None:
        return "possible overlap (audience unknown)"
    if aa.get("everyone") or ab.get("everyone"):
        return "overlap (one sends to everyone)"
    if aa.get("segmentation_id") and aa.get("segmentation_id") == ab.get("segmentation_id"):
        if aa.get("segment") == ab.get("segment"):
            return "same audience"
        return None
    return "possible overlap (different filters)"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("calendar")
    p.add_argument("--audiences")
    p.add_argument("--utc-offset", type=float, default=0.0, help="hours to add to UTC for the project's timezone")
    p.add_argument("--same-channel-hours", type=float, default=24)
    p.add_argument("--cross-channel-hours", type=float, default=4)
    p.add_argument("--busy-day", type=int, default=3, help="flag days with at least this many sends")
    p.add_argument("--include-inactive", action="store_true")
    p.add_argument("--include-webhooks", action="store_true")
    args = p.parse_args()

    sends, skipped = load_entries(args.calendar, args.include_inactive, args.include_webhooks)
    audiences = json.load(open(args.audiences)) if args.audiences else {}
    tz = dt.timezone(dt.timedelta(hours=args.utc_offset))

    def local(ts):
        return dt.datetime.fromtimestamp(ts, tz)

    by_day = defaultdict(list)
    for s in sends:
        by_day[local(s["ts"]).date()].append(s)

    print(f"**Sends in window:** {len(sends)} across {len(by_day)} days (times shown at UTC{args.utc_offset:+g})")
    if skipped:
        print("**Left out:** " + ", ".join(f"{n} {k}" for k, n in sorted(skipped.items())))
    print()
    print("| Day | Sends | Email | SMS | Other | Flag |")
    print("|---|---|---|---|---|---|")
    counts = sorted(len(v) for v in by_day.values())
    median = counts[len(counts) // 2] if counts else 0
    for day in sorted(by_day):
        items = by_day[day]
        ch = defaultdict(int)
        for s in items:
            ch[s["channel"] if s["channel"] in ("email", "sms") else "other"] += 1
        flag = []
        if len(items) >= args.busy_day:
            flag.append("busy day")
        if median and len(items) >= 2 * median and len(items) > 1:
            flag.append("2x median")
        if ch["email"] and ch["sms"]:
            flag.append("email + SMS")
        print(f"| {day:%a %d %b} | {len(items)} | {ch['email']} | {ch['sms']} | {ch['other']} | {', '.join(flag)} |")

    print("\n**Possible collisions:**")
    found = 0
    for i, a in enumerate(sends):
        for b in sends[i + 1:]:
            gap_h = (b["ts"] - a["ts"]) / 3600
            same_channel = a["channel"] == b["channel"]
            limit = args.same_channel_hours if same_channel else args.cross_channel_hours
            if gap_h > max(args.same_channel_hours, args.cross_channel_hours):
                break
            if gap_h > limit:
                continue
            verdict = compare(a, b, audiences)
            if not verdict:
                continue
            found += 1
            kind = f"same channel ({a['channel']})" if same_channel else f"{a['channel']} + {b['channel']}"
            print(
                f"- {local(a['ts']):%a %d %b %H:%M} {a['campaign']} / {a['action']} -> "
                f"{local(b['ts']):%a %d %b %H:%M} {b['campaign']} / {b['action']}: "
                f"{gap_h:.1f} h apart, {kind}, {verdict}"
            )
    if not found:
        print("- None within the thresholds.")

    sms_odd = [s for s in sends if s["channel"] == "sms" and not 8 <= local(s["ts"]).hour < 21]
    if sms_odd:
        print("\n**SMS outside 08:00-21:00 local time:**")
        for s in sms_odd:
            print(f"- {local(s['ts']):%a %d %b %H:%M} {s['campaign']} / {s['action']}")


if __name__ == "__main__":
    main()
