# Discovery query diagnosis

Investigates one underperforming search query. It compares the query's metrics with top queries, looks at the live results, tries other wordings, and checks synonyms, ranking rules, redirects and A/B tests. It then recommends fixes, ranked by estimated impact. It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_query_performance`, `search_discovery_product_grid_insights`, `list_site_search_ranking_rules`, `search_redirects`, `list_site_search_media_rules`, `search_discovery_experiments`, `get_autosuggest_results` |
| **Tested with** | Claude Code (manual run of the method on a demo account) |
| **Maintainer** | Bloomreach |

## Example prompts

- "Why is 'tshirt' converting so badly?"
- "Diagnose the search query 'swim trunks'. It gets no clicks."
- "How can we improve results for 'mens pants'?"

See [examples/tshirt.md](examples/tshirt.md) for a full example output.

## Notes and limitations

- Product grid responses are very large, so the skill asks for only a few fields and rows.
- Product grid calls can fail if run in parallel, so the skill runs them one at a time.
- Impact estimates are upper bounds, not forecasts.
- It works well alongside [discovery-search-health](../discovery-search-health/), which finds queries worth diagnosing.
