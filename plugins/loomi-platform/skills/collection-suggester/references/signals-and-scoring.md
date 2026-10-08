# Signals, thresholds and scoring

Read this in steps 2–4 and 7 of the skill.

## Demand: baseline-adjusted growth

As in the `discovery-trending-searches` skill:

- **expected** = previous sessions × (1 + baseline ÷ 100), where the baseline is the overall change in search sessions (`trends.browse_sessions` from `get_discovery_search_performance`).
- **vs baseline** = current ÷ expected − 1
- **trend score** = (current − expected) ÷ √expected

Use **both** a 30-day window (volume, stable enough to judge conversion) and a 7-day window (what is moving now). On a site whose traffic grew 57% in 30 days, almost every query looks "up 50%+"; only the baseline-adjusted figure means anything.

## Underserved demand (signal b)

A query is **underserved** when shoppers search, the catalog has something, but the page doesn't land. Compare it with the median of the top 20 queries:

| Pattern | Signal | Collection opportunity? |
|---|---|---|
| **Partial match** | conversion under 75% of the median, or bounce over 1.5× the median, **and** the grid returns relevant products (judge the titles) | Yes: a tighter collection page, or a redirect to one |
| **Wrong products** | the grid returns many products but the titles are off-topic (common in hybrid mode) | Maybe: only if a rule finds the right ones |
| **Catalog gap** | nothing relevant in any wording, in `search_mode="standard"` and `"hybrid"` | No: report it as an assortment gap |
| **Synonym gap** | another wording finds the products | No: a synonym fix. Point to `discovery-zero-results-triage` |

Use the method from `discovery-zero-results-triage`: try 2–3 wordings, and at least one in `search_mode="standard"`, before you call something a gap.

## Grouping queries into themes (signal a)

Group by **what the products share**, not by words.

1. For each candidate query (rising, high-volume or underserved), call the product grid with the query, `rows=1`, `fl="pid"` and facets on. If the response is saved to a file, run `scripts/preview_summary.py` on it. Otherwise note the facet values held by 30% or more of `numFound`.
2. Join queries that share at least two dominant values, such as the same leaf category plus the same colour, style or material. A category and its parent count as one. `scripts/group_themes.py` does this and adds up the demand.
3. Check the result makes sense to a shopper. "camo pants", "camouflage trousers" and "camo tshirt" belong together even if their categories differ (the shared trait is the print); "black dress" and "black pants" don't, even though they share a colour.

When the shared trait lives only in titles (no facet carries it), the theme is still real, but no rule can express it. See `rule-syntax.md`, section 5.

## Rising products (signal c)

From `get_discovery_product_performance_table` (sort by revenue, `page_size=100`), rank products by the same baseline-adjusted trend score on revenue, using the top-100 revenue growth as the baseline. Then look for **clusters**: several rising products that share a category, style or colour suggest a collection. One rising product is not a collection.

`get_discovery_products_overview` gives the overall product-driven revenue trend for context.

## Co-purchase affinity (optional, Engagement)

Only if the user wants it and the Engagement project allows it.

1. Resolve the project (`list_cloud_organizations`, `list_projects`; ask if there's more than one).
2. Call `get_event_schema` and look for a purchase line-item event, often `purchase_item`, with `product_id`, `category_level_1`/`_2`, `brand` or `categories_path`. If purchases carry only `product_ids` lists, aggregate EQL can't break them down by item. Say so and skip this signal.
3. The aggregate query is a **customer-level** affinity, not "bought in the same order". EQL can't pair items within an order. For customers who bought from category A, which other categories did they buy from?

   ```
   select count event purchase_item by event purchase_item.category_level_2 grouping top 10
     customers matching exists[event purchase_item where .category_level_2 == "<A>" in last 90 days]
   ```

4. **Call `estimate_eql_cost` first**, and tell the user the level. On a large project this query rated `very_high` (lifetime scan of every item event). Run it only if the user agrees; allow at least 3 seconds between EQL calls.
5. Never read individual customer records. Only aggregate counts go in the output.

## Existing collections (signal d)

For every dynamic category (`search_dynamic_categories`, then one call per ID):

| Check | How | Flag |
|---|---|---|
| Empty | product grid, `search_by="category"`, `query=<categoryId>`, `rows=1`, facets off | `numFound = 0`: **broken**. Read the conditions for impossible values, such as `rating ≥ 40` on a 0–5 scale |
| Thin | same | under 12 products. Check that the condition values exist; for example `gender = female` may be stored as "women" |
| Manual | `rules: []` with `productIds` set | won't update itself as stock changes |
| Not in navigation | `paths` empty or `[[]]`, or missing from `list_categories` | only reachable by direct link |
| Test or demo | names like "test_…" or "demo …" | shouldn't be live |
| Duplicate of a suggestion | a preview's `category` facet lists the existing collection with a share above 70%, **and** the existing collection is a similar size (check its `numFound`) | extend or rename the existing one instead of adding another |

Catch-all collections ("Under $200", "all products") overlap with everything; a high share with one of those isn't duplication.

## Size and quality of a preview

| Measure | Rule of thumb |
|---|---|
| Products | under 12: **too thin**; 12–23: one screen, acceptable for a focused edit; 24–500: good; over 500: **too broad** (it's just a category; tighten the rule) |
| Repeated titles | over 15% of the first 24: variants listed as separate products. Suggest grouping or a ranking rule that buries repeats |
| Brand spread | one brand over 50% of products: a brand page, not a collection; fine only if intended |
| Off-theme items | any obviously wrong product in the top 10 (for example shorts in a trousers edit). Tighten the rule or note the data error |

## Prioritising suggestions

Rank suggestions by this, in order:

1. **Demand at stake:** combined 30-day sessions of the theme's queries. For underserved queries, the upper bound is sessions × (median conversion − theme conversion) × average order value. Say it's an upper bound, not a forecast.
2. **Momentum:** vs-baseline growth over 7 and 30 days.
3. **Feasibility:** a clean rule with 24+ products beats a manual list or a thin edit.
4. **Timing:** a seasonal moment within the next 8 weeks moves a suggestion up.

Fixes to broken existing collections go in their own section, ahead of new suggestions when they are cheap (a wrong condition value).
