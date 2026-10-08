# Finding new products

Read this in steps 2–4 of the skill. Everything marked "checked" was tested live, read-only, on a demo apparel account (account level, no sites) in October 2026. Attribute names differ between catalogs, so always confirm them on the account you're working on.

## 1. Where release data lives

The product performance table has **no release or created date**. Release data comes from catalog attributes, which you reach through the product grid and the catalog tools.

| Where to look | How | What it showed (checked) |
|---|---|---|
| Grid facets | `search_discovery_product_grid_insights`, `query="*"`, `rows=1`, `fl="pid"`, facets on | A `released_since` facet: "New this week" 720, "1-4 weeks" 1,361, "1-3 months" 1,974, "More than 1 quarter" 2,576 (6,631 in total) |
| Attribute list | `list_facet_attributes` via `call_tool`, `only_facetable=false` | `days_since_release` (NUM), `released_since` (STR), `is_new` (STR) |
| One product's record | `search_discovery_catalog_products` with `catalog_name` and `product_id` | `days_since_release: 0`, `is_new: "Yes"`, `released_since: "New this week"`, plus `start_date`/`end_date` epoch values |

Common names in other catalogs: `release_date`, `launch_date`, `created_at`, `date_added`, `first_available`, `new`, `new_arrival`, `season`. A `season` or `collection` value ("AW26") is a weak signal; say so if it's all you have.

**Check that a date is really the release date.** On the demo account, `start_date` was in May 2025 for a product with `days_since_release: 0` and "New this week". It's a promotion or listing date, not a release date. Prefer an explicit age or release field.

**`list_facet_attributes` may not list every attribute.** With `only_facetable=false` it still returned only facetable attributes; `start_date` and `end_date`, which appear in the product record, were missing. Always look at one product record as well.

**`fl` can't return every attribute.** `fl="pid,category_paths"` returned no `category_paths`; `days_since_release`, `released_since` and `is_new` were returned. Get a product's categories from `search_discovery_catalog_products` or from the grid's category facet.

## 2. Filter syntax (checked)

| Filter | `fq` | Result |
|---|---|---|
| Numeric age (best) | `days_since_release:[0 TO 30]` | 2,081 products |
| Buckets | `released_since:"New this week"` | 720 |
| Several buckets | `released_since:"New this week" OR released_since:"1-4 weeks"` | 2,081 (OR inside one string works) |
| Flag | `is_new:"Yes"` | 2,081 (the same set as ≤ 30 days here) |
| New products in one category | `extra_params={"fq": ["days_since_release:[0 TO 30]", "category:\"10600\""]}` | a list ANDs the filters. **AND inside one string returns 0.** |

Bucket labels map roughly to days: "New this week" = 0–6, "1-4 weeks" = 7–30, "1-3 months" = 31–90. Use the numeric field when it exists, so the window can be any length.

Also useful:

- **New products in every category in one call**: `query="*"`, the release `fq`, `rows=1`, facets on. The `category` facet then counts new arrivals per category (facets on fields you didn't filter are filtered). Compare it with the same call without `fq` (`scripts/new_by_category.py`).
- **New products among a query's or category's results**: run that grid with facets on and read the release facet (`released_since` here). That's the share of new products among all matches, which `scripts/new_in_grid.py` compares with the first page.

## 3. Listing the new products (checked)

- Page with `rows=200` and `start` (0, 200, 400 ...), one call at a time, `fl="pid,title,brand,price,days_since_release"`, `extra_params={"facet":"false"}`. Each page was about 80,000 characters.
- `rows=500` and `rows=1000` returned **HTTP 500**. Stay at 200.
- Paging `query="*"` with the same filter was stable: 11 pages gave exactly 2,081 unique product IDs, matching `numFound`.
- A short last page may come back inline instead of being saved to a file. Save its IDs (and ages) as text lines, `pid,days`; the scripts accept both.

## 4. Sanity checks on the release data

Run these before trusting the list. `scripts/new_arrivals.py` does the first one for you.

1. **Views before release.** The previous period of the product table is the window just before the current one. A product released inside the current window can't have views in the previous one. On the demo account, **all 2,000** "new" products with an age had previous-period views, and new arrivals held exactly the same share of views in both periods (33.9%). The release attribute there is synthetic and doesn't match traffic. When more than half conflict, report the data as unreliable, judge every product on the whole window, and recommend a feed fix.
2. **Implausible volume.** 31% of a catalog released in 30 days, or hundreds of products all aged 0, suggests the age is recalculated or reset on every feed load. Check whether the age moves day by day (compare a product's value on two days) before building a rule on it. Not verified on the demo account.
3. **Catalog counts.** `search_discovery_catalogs` reported 8,183 product documents while the grid's `numFound` for `*` was 6,631. Use the grid count for "products shoppers can find", and mention the gap if it's large: unsearchable or filtered-out products can't be seen at all.

## 5. When there's no release data

Say so plainly, then use the fallback: products with views this period and **none** in the previous period (`scripts/new_arrivals.py --fallback-no-prev`). Caveats to state:

- It also catches products back in stock, relaunched or newly categorised.
- It misses new products with no views at all (they're not in the table). Compare the grid's catalog count with the table's `total_rows`; a gap means unseen products, new or not.
- On the demo account the fallback found none (every product had views in both periods, at 30 and at 7 days).

Recommend adding a release date (or age) attribute to the feed, with the catalog owner and the `data-feed-health` skill.

## 6. Existing new-arrivals collections (checked)

- `search_dynamic_categories` with `query="new"` matched by name only: on the demo account it found "New Radiance Collection", whose rule was `collection ANY_MATCH "Radiance"`, nothing to do with release dates. Always fetch by `category_id` and read `conditionConfig.rules`.
- The list view's `conditionConfig` is null and `productIds` is empty. Fetching by ID gives the rules; `productIds` stays empty even then. Preview the collection with the grid (`search_by="category"`, `query=<brg_dyn_ ID>`).
- `list_categories` returns IDs **lower-cased** in `categoryId` (`1002a0`), while the grid and `originalCategoryId` keep the original case (`1002A0`). Use `originalCategoryId` with the grid.
- The responses include editor names and email addresses. Never repeat them.

A good new-arrivals collection is **rule-based on the release attribute**, so it refreshes itself. Dashboard condition shapes seen on this account: `{"level": "PRODUCT", "attribute": "<name>", "operator": "ANY_MATCH" | "LESS_THAN_OR_EQUAL" | "GREATER_THAN_OR_EQUAL", "values": [...]}`. Suggested rules (not created or verified as dynamic categories):

- numeric age: `days_since_release LESS_THAN_OR_EQUAL 30`;
- buckets: `released_since ANY_MATCH ["New this week", "1-4 weeks"]`;
- flag: `is_new ANY_MATCH ["Yes"]`.

Hand off to `collection-suggester` for the preview, the readable and dashboard forms of the rule, and the set-up steps. No Loomi Connect tool creates dynamic categories.
