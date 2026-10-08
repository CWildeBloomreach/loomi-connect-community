# Rules, previews and dashboard set-up

Read this when you write a collection's rule, preview it in the product grid, or give set-up steps. Everything below was checked live on a demo apparel account in October 2026. Attribute names differ between catalogs, so always confirm them against the account's own facets and existing dynamic categories.

## 1. Which attributes you can use

Build rules only from attributes the catalog actually fills in.

- **Facets returned by the product grid** (`data.facet_counts.facets[].name`) are the attributes you can filter on with `fq`. Typical names are `category`, `brand`, `colors`, `style`, `material`, `season`, `gender`, `onSale`, `price` and `rating`. Some facets, such as `gender` on a dresses page, only appear where a category facet rule switches them on.
- **Existing dynamic categories** show the names the category builder uses. Fetch a few with `search_dynamic_categories` and `category_id` and read `conditionConfig.rules[]`.
- **Product titles are not filterable.** `fq=title:"camo"` returned 0 even though 10 products have "camo" in the title. If a theme exists only in titles (a print, a fabric, a cut), there is no rule for it yet. See section 5.

**Check coverage before you trust an attribute.** On the demo account, only 40 of 1,219 men's trousers had a `style` value, and 52 of 58 "khaki pants" results had `colors = multi`. A rule built on a sparsely filled attribute misses most of the products the shoppers want. Report this as a data gap.

## 2. Previewing a rule in the product grid

Call `search_discovery_product_grid_insights` one call at a time, always with a small `fl`.

| What the rule says | How to preview it |
|---|---|
| One attribute, one or more values | `query="*"`, `fq='colors:"khaki" OR colors:"olive"'` |
| A category and one attribute | `search_by="category"`, `query="<category id>"`, `fq='colors:"beige" OR colors:"cream"'` |
| Several conditions joined with AND | `query="*"` and `extra_params={"fq": ["category:\"20200\"", "colors:\"olive\""]}`. Each list item is sent as its own `fq`, and the grid ANDs them. Each item can contain ORs. |
| A price cap | `extra_params={"fq": ["price:[* TO 50]"]}` (range syntax not verified live; check `numFound` looks sensible) |

**Don't put AND inside a single `fq` string.** `fq='category:"20200" AND colors:"khaki"'` returned 0 every time, even when matching products existed. OR inside one string works.

**Facet counts for a filtered field are unfiltered.** If `fq` filters on `colors`, the `colors` facet in the same response still shows counts for the whole catalog or category (multi-select behaviour). Every other facet is filtered. This is a cheap way to see the full value list for an attribute: `query="*"`, `fq` on that attribute, `rows=1`.

**Colour facets count variants.** A product with a black and a yellow variant counts under both, so colour counts can add up to more than `numFound`.

Sizes:

| Purpose | Settings | Typical size |
|---|---|---|
| Count only | `rows=1`, `fl="pid"`, `extra_params={"facet": "false"}` | 5–10k characters |
| Attribute profile (for grouping) | `rows=1`, `fl="pid"`, facets on | 15–50k characters (the `rating` facet is long) |
| Full preview | `rows=10`, `fl="pid,title,brand"`, facets on | 25–60k characters, often saved to a file |

Keyword-mode responses carry a long per-product debug explanation, so a keyword grid with `rows=12` can be as large as a category browse with `rows=24`. Never pass `simple_debug=false` (HTTP 500).

## 3. Dynamic category conditions (what the dashboard stores)

`search_dynamic_categories` with `category_id` returns:

```json
"conditionConfig": {
  "operator": "AND",
  "rules": [
    {"level": "PRODUCT", "attribute": "category_id", "operator": "ANY_MATCH", "values": ["21200"]},
    {"level": "PRODUCT", "attribute": "style", "operator": "ANY_MATCH", "values": ["Formal"]}
  ]
}
```

Observed values:

| Field | Values seen |
|---|---|
| `operator` (top level) | `AND`, `OR` (one operator joins all rules) |
| `level` | `PRODUCT`, `VARIANT` (colour was `VARIANT`) |
| rule `operator` | `ANY_MATCH`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN_OR_EQUAL` |
| `attribute` | `category_id`, `style`, `color`, `gender`, `onSale`, `sale_price`, `rating`, `collection` |

The facet and condition names don't always match: the grid facet `colors` is the condition attribute `color`, and the facet `category` is the condition attribute `category_id`. A category with `rules: []` and a list of `productIds` is a **manual** collection: it never updates itself.

Write each suggested rule in both forms:

- **Readable:** `category = /men/pants AND color IN (beige, cream, taupe, khaki, olive)`
- **Dashboard conditions:** the `conditionConfig` shape above, using the condition attribute names.

## 4. Set-up steps for the Discovery dashboard

No Loomi Connect tool creates or edits dynamic categories (checked with `search_tools` in October 2026). Give the user these steps:

1. In the Discovery dashboard, open **Merchandising → Categories** (the dynamic category builder; the menu label can vary by account).
2. Create a new dynamic category with the suggested name and the catalog shown in the preview (`catalogName`).
3. Add each condition: attribute, operator, values, and **product or variant level** as listed. Set the top-level match to AND or OR.
4. Save, wait for the sync, then check the product count matches the preview (within a few products; variant-level conditions can differ slightly).
5. Decide where it appears: add it to the navigation tree (otherwise it has no path and shoppers can reach it only by direct link), point a redirect at it, or use it as a recommendation or email feed.
6. Optional: add a category ranking rule (for example, bury repeated titles or boost in-stock sizes), and run an A/B test if the collection replaces an existing page.

## 5. When no rule is possible

If the shared trait lives only in titles or descriptions:

- **Short term:** a manual collection (a fixed list of product IDs, like the demo account's "Heritage" category). Say clearly that it **won't update itself** and needs someone to maintain it.
- **Fix:** add or fill the attribute in the product feed (for example a `pattern` attribute with "camo", or map "khaki" to a colour value). Recommend the `data-feed-health` skill and the catalog owner.
- **Meanwhile:** a redirect from the theme's queries to a search results page for the best-performing wording.
