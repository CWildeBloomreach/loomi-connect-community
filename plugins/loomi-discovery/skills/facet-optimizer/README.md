# Facet optimizer

Reviews the filters (facets) shoppers see on a Bloomreach Discovery account's top search and category pages. It reads each page's live facets from the product grid, the global, search and category facet rules, and the list of facetable attributes. It flags junk facets (empty, too many values, unbucketed numbers, internal fields), useful facets that are missing or buried for a product type (size, colour, price, gender, fit), and values that need merging or tidying. It recommends boost, bury, hide and always-show changes by scope (global, product type, single query or category), and never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_query_performance`, `get_discovery_category_performance_table`, `search_discovery_product_grid_insights`, `list_facets_global`, `list_site_search_facets`, `list_category_facets`, `get_facet_rule`, `list_facet_attributes` (via `search_tools` / `call_tool`) |
| **Tested with** | Claude Code (manual, read-only run of the method against a demo Discovery account with no sites, at account level: 3 search pages, 2 category pages, 4 facet rules, 44 facetable attributes; about 15 calls). Not yet tested in an OpenAI client, and not yet run end-to-end from the skill file in a fresh session |
| **Maintainer** | Bloomreach |

## Example prompts

- "Review the filters on our top search pages."
- "Which facets should we show on the jeans category?"
- "Why is the rating filter so long?"
- "Are any of our facets hurting conversion?"

See [examples/example-apparel.md](examples/example-apparel.md) for a full example output.

## What it found in testing

- A global rule always showed a colour-group facet that was empty on every page, and configured price ranges, but no price facet appeared on any page.
- The rating facet listed raw values (43 values for 43 dresses), and "1.0" covered 27–37% of products: a placeholder, not a rating. A category rule boosted it to second place.
- An internal "cluster" facet (values "c18", "c69") showed on every page, and `margin` and nine `omni_score_*` fields were facetable.
- "pants" and "jeans" span men's and women's products but showed no gender filter; size came last on "jeans" and covered only 52 of 1,170 products.
- Brand and colour values needed merging ("Pacific" / "Pacific ", "gray" / "grey"), and test and campaign categories appeared in the category filter.

## Notes and limitations

- Product grid responses are large (25,000–60,000 characters with `rows=1`). The skill keeps facets on, asks for one row, and includes `scripts/facet_summary.py` (standard library only, no network) to summarise saved responses and flag problems.
- Range buckets, value merging and renaming can't be set through the API; the skill marks those recommendations as dashboard changes.
- The skill can't measure how a facet change will affect conversion. It reports the sessions affected and recommends A/B tests for large changes.
- `get_facet_rule` returns the last editor's name or email; the skill never repeats it.
