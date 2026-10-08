# Brand performance review

Builds a brand scorecard for a Bloomreach Discovery account. For each brand it compares the share of revenue with the share of views and of first-page search slots, separates real exposure problems from price effects, tracks each brand against the account's own trend, and checks brand-name searches and where brands rank on their main queries. The output gives buyers factual talking points for supplier and co-op marketing conversations, and gives merchandisers ranking recommendations with revenue at stake. It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_brand_performance`, `get_discovery_product_performance_table`, `get_discovery_products_overview`, `get_discovery_query_performance`, `search_discovery_product_grid_insights` |
| **Tested with** | Claude Code: a manual read-only run of the method against a demo account at account level (no sites). Site-level reporting wasn't tested |
| **Maintainer** | Bloomreach |

## Example prompts

- "Give me a brand scorecard for this month."
- "Which brands should we boost or bury?"
- "I'm meeting Tommy Hilfiger next week. How are they doing with us?"
- "Which brands do people search for that we don't convert?"

See [examples/example-apparel.md](examples/example-apparel.md) for a full example output.

## Scripts

Both scripts use only the Python standard library and never touch the network.

- `scripts/brand_scorecard.py`: joins the brand, product and query tables and the first-page grids into a scorecard, with exposure and conversion indices, trend against the account, brand-name search performance, flags and revenue at stake.
- `scripts/grid_positions.py`: reads a saved product grid and reports how many products each brand has for the query, how many are on the first page, and their best and median positions.

## Notes and limitations

- Visibility means product page visits; Loomi Connect doesn't expose impressions. First-page shelf share on the top queries fills part of that gap.
- An expensive brand earns more per view even when it converts normally, so the skill requires conversion to agree before calling a brand under- or over-exposed.
- In testing, `get_discovery_brand_performance` (30-day window) returned previous-period totals that didn't match the product table or the overview, so the skill takes trends from the product table and warns when they disagree.
- Brand-name search matching is by whole words; brand names that are everyday words ("AND", "Basics") must be excluded with `--ignore`.
- Revenue at stake is an upper bound for the period, not a forecast.
- Hand-offs: [discovery-experiment-setup](../discovery-experiment-setup/) for boost and bury tests, [discovery-query-diagnosis](../discovery-query-diagnosis/) for brand queries that return the wrong results. For product-level boosts and buries, see [product-opportunity-finder](../product-opportunity-finder/).
