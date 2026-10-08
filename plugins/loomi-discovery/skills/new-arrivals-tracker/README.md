# New arrivals tracker

Answers "are our new products getting seen?" for a Bloomreach Discovery account. It finds the products released in the last N days (default 30) from the catalog's release attributes and checks that those dates match traffic. For each new product it measures views, add-to-cart, conversion and revenue, and checks where it ranks on its category and main search. It then sorts each product into **breakout** (promote and restock), **buried** (boost candidate), **slow start** (fix the page, price or images) or **invisible** (fix the data or categorisation). It compares new arrivals as a group with the rest of the catalog, shows which categories carry them, checks any existing new-arrivals collection, and recommends boosts, data fixes and whether to build a new-arrivals collection. It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `search_discovery_product_grid_insights`, `search_discovery_catalogs`, `search_discovery_catalog_products`, `list_facet_attributes` (via `search_tools` / `call_tool`), `list_categories`, `search_dynamic_categories`, `get_discovery_products_overview`, `get_discovery_product_performance_table`, `get_discovery_query_performance` |
| **Tested with** | Claude Code: a manual read-only run of the method against a demo account at account level (no sites), October 2026. On that account the release data failed the skill's check (every "new" product had earlier views), so the age-adjusted path, the invisible group and the no-views path were tested only with small hand-made fixtures. Site-level reporting, a live existing new-arrivals collection and the `--positions` re-run on a real launch weren't tested |
| **Maintainer** | Bloomreach |

## Example prompts

- "Are our new arrivals getting seen?"
- "How are the products we launched this month doing?"
- "Which new products should we promote, and which aren't selling?"
- "Do we need a New In collection?"

See [examples/example-apparel.md](examples/example-apparel.md) for a full example output.

## Scripts

All scripts use only the Python standard library and never touch the network.

- `scripts/new_arrivals.py`: checks the release data against traffic, compares new arrivals with the rest of the catalog (shares of products, views and revenue; visibility index, age-adjusted when the dates are trustworthy), and sorts each new product into breakout, buried, slow start, invisible, too early or on track, with the revenue-at-stake working. Has a fallback for catalogs with no release data.
- `scripts/new_by_category.py`: compares the category facet of the whole catalog with that of new arrivals, and flags categories with no, few or mostly new products.
- `scripts/new_in_grid.py`: for a saved category or query grid, gives each new product's position, how many new products reach the first page, and a placement index (new share of the first page ÷ new share of all results).
- `scripts/grid_positions.py`: the same script as in `product-opportunity-finder`: positions, first-page brand mix, ranking rules and A/B test status.

## Notes and limitations

- The product performance table has no release date and no impressions. Release data comes from catalog attributes (here `days_since_release`, `released_since` and `is_new`), and "seen" means product page visits.
- The table leaves out products with no views in either period, so a new product missing from it had no views at all.
- Product grid lists are paged at 200 rows; 500 or more returned HTTP 500 in testing.
- Revenue at stake is an upper bound for the period, not a forecast.
- Hand-offs: [discovery-experiment-setup](../discovery-experiment-setup/) for boosts, [collection-suggester](../../../loomi-platform/skills/collection-suggester/) for a new-arrivals collection, [discovery-category-health](../discovery-category-health/) for category pages, [product-opportunity-finder](../product-opportunity-finder/) for the whole catalog, and `data-feed-health` for release-data fixes.
