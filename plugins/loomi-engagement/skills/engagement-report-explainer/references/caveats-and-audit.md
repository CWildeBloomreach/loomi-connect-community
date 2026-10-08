# Caveats and audit checks

Apply these to each analysis. Use the smallest set of calls that answers each check. Report a finding only when the evidence supports it, and say what you didn't check.

## Severity

- **Action:** probably wrong or broken now. Fix or archive it.
- **Review:** may be intended, but a person should confirm before trusting the numbers.
- **Info:** worth knowing when reading it, no action needed.

## From the list alone (no extra calls)

| Check | Rule | Severity | Suggested action |
|---|---|---|---|
| Not touched in a long time | `edited` more than 365 days ago | Info | Confirm the events and filters are still current |
| Archived but in use | `archived: true` and it appears on a dashboard (or in a segmentation's `used_by`) | Action | Restore it or remove it from the dashboard |
| Duplicate-looking names | names that differ only by "copy", "v2", "test", "old", a date | Review | Keep one source of truth |
| Parametrized with no saved values | `parametrized: true` (check `parameter_values` in the definition) | Review | The numbers depend on what's typed in; say which values you used |

Use 365 days as the default and change it if the user gives another threshold.

## From the definition

| Check | Rule | Severity |
|---|---|---|
| Stale fixed window | a date filter with `enabled: true`, `absolute: true` and `to_date` more than 30 days ago, on an analysis whose name suggests "current", "last N days", "this month", "YTD", or that sits on a dashboard | Action: it stopped updating on that date |
| Name and window disagree | the name says "30D", "weekly", "YTD" and the window says otherwise | Review |
| Window switched off | a date filter with `enabled: false` (so all time) while a `duration` is filled in | Info: say it's all-time; Review if the name suggests a period |
| No conversion window | funnel `duration_filter.enabled: false` | Info: a customer can convert months later and still count |
| Silent exclusion | a filter (report-wide, per-metric or customer filter) that limits to one value of channel, source, platform, device, country, language, store or currency, or excludes one | Review: say exactly who's left out |
| Hard-coded IDs or test values | filters on specific campaign IDs, customer IDs, email domains or test flags | Review: brittle, and may hide new campaigns |
| Events not people | `aggregation: count` with `occurrence_per_customer: all` on a metric whose name says "customers", "users" or "buyers" | Review: counts events, so repeat actions are counted many times |
| Ratio denominator | a formula metric (`V0/V1`) where V1 has a different filter or window from V0, or where the name says "rate" but there's no division | Review: say what the rate is really out of |
| Revenue double counting | summing an item-level event (`purchase_item`) and calling it orders, or summing `cart_update.total_price` (a running cart total) | Action |
| Missing reference | an `expression`, `aggregate`, `prediction`, `segmentation` or customer filter `id` that isn't in its list | Action |
| Archived reference | a referenced segmentation or other object with `archived: true` | Action |
| Event no longer tracked | an event type that isn't in `get_event_schema` (check only when the user asks or the numbers are zero) | Action |
| Segment order | a segmentation whose earlier segments are broad enough to swallow later ones | Review |
| Global pre-filter | a segmentation with a non-empty global `customer_filter` | Info: customers outside it are in no segment |

## Dashboards

| Check | Rule | Severity |
|---|---|---|
| Mixed windows side by side | tiles next to each other with different windows (1 hour vs 30 days, rolling vs fixed) and headings that don't say so | Review |
| Missing embedded analysis | a component `id` the matching `search_*` tool can't find | Action |
| Unreadable tiles | `metric` components | Info: "definition not readable through Loomi Connect" |
| Static reference text | an `html` or `text` block with thresholds, targets or dates | Info: may be out of date; say what it claims, without names or emails |
| Not shared | `shared: false` on a dashboard the user calls "ours" | Info: others in the team may not see it |

## Numbers (only when you calculated them)

| Check | Rule | Severity |
|---|---|---|
| Empty or all-zero result on production | `as_dict` empty or all zeros | Review: likely a cold cache or a stale/broken definition; open it in the UI to warm it |
| Last bucket is partial | a time series whose last bucket is today | Info: today isn't finished, so it looks like a drop |
| Sparse data | most buckets are zero | Info: small numbers swing a lot; avoid reading trends into them |
