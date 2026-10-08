# Cause checklist

Work through these in order. For each, record what you checked, what you found, and how much of the change it could explain. "Checked, nothing found" is a useful result: list it under "Checked and ruled out".

The **window** is from the start of the comparison period to the end of the current period. Rule and experiment timestamps are Unix milliseconds; convert them to dates in UTC.

## 1. Data problems (check first)

A tracking or catalog problem makes every other number unreliable.

| Signal | Where | What it means |
|---|---|---|
| Days missing from `get_discovery_trend`, or showing $0 revenue, in either period | the script's `trend.data_gaps` | A reporting or tracking outage. A "rise" or "fall" across those days isn't real. Choose a period without gaps |
| `conversion-pageview` count changes much more than the orders on the overall card | `get_pixel_health_status`, 168 h vs (336 h − 168 h) | Order tracking broke or was double-firing. Revenue "changed" in reporting, not in reality |
| A core pixel type's issue rate jumped (from under 1% to over 5%) | same | A front-end release broke a pixel parameter. Offer `data-feed-health` |
| A core pixel type fell to zero | same | Pixel removed from a page template |
| Failed product feed or index job, or `stats.product_doc_count` fell by 10% or more | `search_discovery_catalog_jobs` | Products missing from search and category pages |
| Feed warnings ("Feed data contains null values") | same | Usually minor; mention it only if the same products appear among the fallers |

The pixel window ends **now**, while the dashboard ends a day or two earlier. Differences under about 5% are not evidence.

A pixel type stuck at a 100% issue rate in **both** weeks (for example `search-pageview` flagged `catalogs_required`) is a standing problem, not a cause of this change. Mention it as a caveat.

## 2. Merchandising rules

Lists: `list_site_search_ranking_rules`, `list_category_ranking_rules`, `list_ranking_rules_global`, `search_redirects`, `list_site_search_media_rules`, `list_category_media_rules`. Sort by `lastModifiedAt` descending.

Keep a rule if **any** of these falls in the window:

- `lastModifiedAt` or `createdAt`: someone edited or created it;
- `startedAt`: a scheduled rule switched on, even if nobody edited it then;
- `endedAt`, or `durationTag="expired"` with an end date in the window: a rule switched off.

Then match it to the contributors:

- a site search rule's `queries[].query` against the query table (a phrase-match rule on "shirt" also affects "shirt women" and "collared shirt": check those too with `get_discovery_query_performance` and `search=<term>`);
- a category rule's `queries[].query` is a category ID: match it to `cat_id` in the category table;
- a global rule (`*`) affects everything; look for a step in the daily trend on its date.

Judge it:

- **Strong:** the matched query or category is among the top fallers or risers, its change started on the rule's date, and its main driver fits (a ranking rule usually moves conversion or order value, not traffic; a redirect removes the query from the table altogether).
- **Weak:** the matched query or category barely moved, or the timing doesn't fit.

`lastModifiedAt` also changes when someone saves a rule without changing it. Use `get_ranking_rule` on a strong candidate to see what it does.

## 3. A/B tests

`search_discovery_experiments` with `sort_by="STARTED_AT"`. Look for:

- a test that **started** in the window: part of the traffic for its query or category now sees a different rule;
- a test that **ended** in the window: with a winner, the winning variant now gets 100% of traffic; without one, traffic returns to default;
- a test **running** across both periods: not a cause of change on its own.

Each bucket's `ruleIdentifierInfo.query` names the query or category ID. Match it to the tables as for rules. For results, offer `discovery-experiment-readout`.

## 4. Demand and mix (no site change)

If no rule, test or data problem lines up, the change is usually about demand:

| Pattern | Likely explanation |
|---|---|
| Traffic explains most of it, on every device and channel alike | Fewer visitors: seasonality, marketing spend, paid traffic, a holiday. Check with whoever runs acquisition and email (`engagement-campaign-digest`) |
| Order value explains most of it, conversion steady | Mix shift to cheaper items, or a promotion. Look at which high-price queries, categories or brands fell |
| Conversion falls on one device only | A device-specific front-end or checkout problem. Check that device's pixel issue rate and the site's release notes |
| Conversion falls across many queries at once | Price, stock or checkout, not search. Hand to the merchandising or product page team |
| A cluster of related queries and categories moves together (for example diamond, rings, bracelets) | A theme: a stock-out, price change or promotion in that range |
| One or two days account for most of it | An outage, a flash sale in the comparison period, or a big email send. Check what happened on those dates |
| The comparison period was unusually strong | Not a drop, but a return to normal. Check the 28-day trend |

## 5. Confidence

- **High:** timing, size and mechanism all line up, and nothing else explains it.
- **Medium:** two of the three.
- **Low:** plausible but small, untimed, or within normal variation.

Never give "High" when the total change is within normal day-to-day variation (`change_vs_noise` below 1).
