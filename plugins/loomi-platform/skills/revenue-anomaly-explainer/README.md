# Revenue anomaly explainer

Answers "why did revenue (or conversion, or order value) change?" for a Bloomreach Discovery account or site, comparing one period with the one before.

- **Breaks the change down with maths that adds up:** traffic × conversion × order value; search, category and other; device; then the queries, categories, products and brands that moved most, each with its share of the change.
- **Checks the likely causes:** merchandising rules edited, started or expired in the window; A/B tests started or stopped; tracking pixel and catalog feed health; and the daily shape of the change (a step, a few days, or spread evenly), including data gaps.
- **Returns a ranked list of causes** with evidence, money explained, confidence and the next step, often pointing to another skill for the deep dive.

It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_overall_performance`, `get_discovery_search_performance`, `get_discovery_category_performance`, `get_discovery_trend`, `get_discovery_query_performance`, `get_discovery_category_performance_table`, `get_discovery_product_performance_table`, `get_discovery_brand_performance`, `list_site_search_ranking_rules`, `list_category_ranking_rules`, `list_ranking_rules_global`, `search_redirects`, `list_site_search_media_rules`, `list_category_media_rules`, `search_discovery_experiments`, `get_pixel_health_status`, `search_discovery_catalogs`, `search_discovery_catalog_jobs` (via `search_tools` and `call_tool`) |
| **Tested with** | Claude Code (manual read-only run of the method on a demo Discovery account with no sites, 7-day window; script tested on that run's saved responses and on synthetic step, flat and zero cases. Not yet tested: a site-level account, `list_ranking_rules_global`, media rule and redirect lists in the window check, paging catalog jobs beyond 50, custom comparison dates, or an OpenAI client) |
| **Maintainer** | Bloomreach |

## Example prompts

- "Why did revenue drop last week?"
- "Conversion fell on mobile this month. What changed?"
- "AOV is down 5% since the 1st. Is it something we did?"
- "Explain the revenue spike on 14 October."

See [examples/example-apparel-week.md](examples/example-apparel-week.md) for a full example output.

## Scripts

- `scripts/decompose_change.py`: reads the saved card, table and trend responses and prints the breakdown as JSON: the traffic / conversion / order-value split (log-mean method, so the parts add up exactly), channel and device splits, top contributors with their share of the parent change and the long-tail remainder, and the daily shape (aligned by date, with data gaps flagged). Standard library only; no network access.

## Notes and limitations

- The headline cards don't say which dates they cover, and data usually ends a day or two before today. The skill reads the dates from the daily trend.
- Search and category revenue overlap (a visit can include both), so "other" is an approximate remainder.
- The daily trend leaves out days with no data; the script pairs days by date and reports gaps instead of treating them as real falls.
- The pixel health window ends now, while the dashboard ends earlier, so small pixel differences aren't treated as evidence.
- Rule and experiment lists include editors' email addresses. The skill never repeats them.
- Confidence levels are judgement, not statistics. The noise check is a rough guide.
- Related skills: [weekly-ecommerce-briefing](../weekly-ecommerce-briefing/) (spots the change), [data-feed-health](../data-feed-health/), and the Discovery skills it hands off to (`discovery-query-diagnosis`, `discovery-category-health`, `discovery-rule-audit`, `discovery-experiment-readout`).
