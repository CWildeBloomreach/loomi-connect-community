# Discovery dynamic category review

Reviews every dynamic (rule-based) category in a Bloomreach Discovery account or site. For each one it reads the definition, counts the products it returns, finds which other categories it overlaps, and checks its traffic and conversion. It flags empty or near-empty categories, overlaps and duplicates of static categories, fragile definitions (a single attribute value, seasonal or campaign tags, hard-coded product IDs, fixed dates), names that don't match the products, and dynamic categories with traffic but poor performance, then returns a prioritised list of fixes. It never changes anything.

It complements [discovery-category-health](../discovery-category-health/), which covers all category pages but checks dynamic categories only for being empty or thin.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `search_dynamic_categories`, `list_categories`, `search_discovery_product_grid_insights`, `search_discovery_catalog_products`, `get_discovery_category_performance_table`, `get_discovery_category_performance`, `search_discovery_experiments` |
| **Tested with** | Claude Code: read-only calls against a demo account to check tool shapes (`list_discovery_accounts`, `search_dynamic_categories` list and by ID, `search_discovery_product_grid_insights` for one dynamic category, `get_discovery_category_performance_table` with `search`, `search_discovery_catalog_products`, `list_categories`). `scripts/review_dynamic_categories.py` tested on synthetic files shaped like those responses. A full end-to-end run, `get_discovery_category_performance`, `search_discovery_experiments`, site-level scoping and OpenAI clients not yet tested |
| **Maintainer** | Bloomreach |

## Example prompts

- "Review our dynamic categories."
- "Are any of our rule-based collections empty, duplicated or out of date?"
- "Which collection landing pages get traffic but don't convert?"
- "Do any of our dynamic categories rely on hard-coded product IDs?"

See [examples/example-apparel.md](examples/example-apparel.md) for an illustrative output.

## Scripts

- `scripts/review_dynamic_categories.py` (Python standard library, no network) reads the saved definitions, product grid responses, performance table and category tree, and prints an inventory plus a prioritised findings table. The checks are also listed in [references/checks.md](references/checks.md) for clients that can't run scripts.

## Notes and limitations

- The `search_dynamic_categories` list view has no conditions, so the skill fetches each category by ID: about two or three calls per category. For large accounts it asks whether to focus on a subset.
- Product counts come from the product grid (`numFound`), not from `search_discovery_catalog_products`, which has no filter. The catalog tool is used only to check attribute values.
- Overlaps come from the grid's category facet. It shows shared product counts cheaply, but may not list every category on very large collections.
- Dynamic category records include creator and editor email addresses; the skill leaves them out of the report.
- Impact estimates are upper bounds, not forecasts.
- Hands off to `discovery-category-health` (ranking, buried products and rules on flagged pages) and `facet-optimizer` (filters on large collection pages).
