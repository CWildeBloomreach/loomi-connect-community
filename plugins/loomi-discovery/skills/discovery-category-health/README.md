# Discovery category health check

The category-page counterpart of [discovery-search-health](../discovery-search-health/). It summarises category page performance, compares every category with like-for-like peers, checks that dynamic categories contain products, reviews category rules, and looks for strong products buried low on key category pages. It recommends fixes but never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_category_performance`, `get_discovery_overall_performance`, `get_discovery_category_performance_table`, `get_discovery_product_performance_table`, `list_categories`, `search_dynamic_categories`, `search_discovery_product_grid_insights`, `list_category_ranking_rules`, `get_ranking_rule`, `list_category_facets`, `list_category_media_rules`, `search_discovery_experiments` |
| **Tested with** | Claude Code (manual read-only run of the method against a demo account at account level; site-level reporting not yet tested) |
| **Maintainer** | Bloomreach |

## Example prompts

- "How are our category pages performing this month?"
- "Which categories are underperforming, and why?"
- "Are any of our dynamic categories empty?"
- "Run a category health check on our Discovery site."

See [examples/example-apparel.md](examples/example-apparel.md) for a full example output.

## Scripts

Both scripts use only the Python standard library and never touch the network. They reshape data the assistant has already fetched.

- `scripts/category_baseline.py`: groups categories into like-for-like peers (dynamic, top-level, sub-category), flags outliers against each group's median, and lists period swings, new categories, same-named categories and tracking problems.
- `scripts/buried_products.py`: matches a category's product grid with product performance to find repeated titles, brands missing from the first screen, and strong products ranked low.

## Notes and limitations

- Category names often repeat across departments, so the skill names categories by path.
- `filter_preset="lowest_converting"` returned no rows in testing, so the skill sorts by conversion instead.
- Passing `simple_debug=false` to the product grid caused HTTP 500 errors in testing, so the skill leaves it on and keeps `fl` and `rows` small.
- The product performance report has no category filter, so buried-product checks match products by ID and cover only the products in the pages fetched.
- Audience-targeted category rules don't show in the default product grid. The rule list doesn't show their audience either, so the skill fetches rule details with `get_ranking_rule`.
- Impact estimates are upper bounds, not forecasts.
