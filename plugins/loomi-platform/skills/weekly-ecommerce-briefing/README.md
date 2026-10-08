# Weekly ecommerce briefing

A one-screen Monday-morning briefing for merchandisers and ecommerce managers, from Bloomreach Discovery and (optionally) Engagement:

- **Headline KPIs**, this week against last: revenue, revenue per visit, conversion and average order value, overall, for search, category and "other", and by device;
- **Top movers:** search queries (measured against overall search growth, the `discovery-trending-searches` method), categories, products and brands;
- **Marketing:** email and SMS send highlights from Engagement (the `engagement-campaign-digest` method, cut down);
- **Health alerts:** tracking pixel and catalog feed problems (the `data-feed-health` method, cut down);
- **Three things to do this week**, each linked to the skill that does it.

You can ask for Discovery only, Engagement only, or both. It never changes anything.

| | |
|---|---|
| **Products** | Discovery, Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_overall_performance`, `get_discovery_search_performance`, `get_discovery_category_performance`, `get_discovery_trend`, `get_discovery_query_performance`, `get_discovery_category_performance_table`, `get_discovery_product_performance_table`, `get_discovery_brand_performance`, `get_pixel_health_status`, `search_discovery_catalogs`, `search_discovery_catalog_jobs` (via `search_tools` and `call_tool`), `list_cloud_organizations`, `list_projects`, `get_campaign_calendar`, `estimate_eql_cost`, `execute_analytics_eql` |
| **Tested with** | Claude Code (manual read-only run: every Discovery section on a demo account with no sites; Marketing on an Engagement sandbox project that had no campaign sends, plus a calendar read on a production project to check the response shape. Not yet tested: a site-level Discovery account, an Engagement project with campaign data in the briefing format, SMS, or an OpenAI client) |
| **Maintainer** | Bloomreach |

## Example prompts

- "Give me the Monday briefing."
- "How did last week go? Search and email."
- "Weekly KPI summary for the team, Discovery only."
- "What should we focus on this week?"

See [examples/example-apparel-briefing.md](examples/example-apparel-briefing.md) for a full example output.

## Scripts

- `scripts/briefing_numbers.py`: reads the saved KPI cards and tables and prints the KPI values (with RPV, conversion and AOV worked out from raw counts) and the top movers as JSON. Standard library only; no network access.

## Notes and limitations

- Discovery data usually ends a day or two before today, so on a Monday the default is the **last 7 available days**, with the dates printed. A calendar week can be requested once it's complete. The two windows can tell different stories.
- Search and category revenue overlap, so "other" is approximate.
- Engagement campaign revenue isn't available from Loomi Connect; the briefing doesn't estimate it.
- The calendar and rule lists include people's names and email addresses. The briefing never repeats them.
- For the "why", use [revenue-anomaly-explainer](../revenue-anomaly-explainer/). For full health checks, use [data-feed-health](../data-feed-health/).
