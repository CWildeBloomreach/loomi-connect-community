# Product opportunity finder

Sorts every product in a Bloomreach Discovery account into five groups a merchandiser can act on: products whose page needs fixing, hidden gems to boost, declining winners, dead weight with no views, and over-exposed products to bury. It checks where the most valuable products rank on their main search queries, works out the revenue at stake for each (with the working shown), and names the skill to hand off to. It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_products_overview`, `get_discovery_product_performance_table`, `get_discovery_query_performance`, `search_discovery_product_grid_insights` |
| **Tested with** | Claude Code: a manual read-only run of the method against a demo account at account level (no sites). Site-level reporting, and the dead-weight path on an account whose catalog is larger than its product report, weren't tested live (the dead-weight script path was tested with sample IDs) |
| **Maintainer** | Bloomreach |

## Example prompts

- "Which products should we boost or bury?"
- "Find me the hidden gems in our catalog."
- "Which of our best sellers are slipping, and why?"
- "Which products get lots of views but don't sell?"

See [examples/example-apparel.md](examples/example-apparel.md) for a full example output.

## Scripts

Both scripts use only the Python standard library and never touch the network.

- `scripts/product_opportunities.py`: sorts the product performance table into the five groups, with confidence checks so small products aren't flagged by chance, a trend-adjusted test for declining winners (and whether visibility or conversion drove the fall), and the revenue-at-stake working for each product.
- `scripts/grid_positions.py`: reads a saved product grid and reports where given products and brands rank, the first-page brand mix, applied ranking rules and any running A/B test.

## Notes and limitations

- The product table has no impressions, so visibility means product page visits. It also doesn't say whether a visit came from search, a category page or recommendations, so the skill checks rankings before recommending a bury.
- Products with no views may be missing from the product table altogether, so the skill compares it with the catalog count from the product grid (`query="*"`).
- Declining winners are judged against the account's own revenue trend. In a growing period, a product can gain revenue and still be losing ground.
- Revenue at stake is an upper bound for the period, not a forecast.
- Hand-offs: [discovery-experiment-setup](../discovery-experiment-setup/) for boost and bury tests, [discovery-query-diagnosis](../discovery-query-diagnosis/) when a product's main query looks broken.
