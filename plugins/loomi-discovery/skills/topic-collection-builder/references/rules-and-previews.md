# Rules, previews and dashboard set-up

Read this when you write a collection's rule, fetch its products in the product grid, or give set-up steps. These behaviours were checked live on a demo apparel account in October 2026 (see also `collection-suggester`, which uses the same method). Attribute names differ between catalogs, so confirm them against the account's own facets and existing dynamic categories.

## 1. Which attributes you can use

- **Facets returned by the product grid** (`data.facet_counts.facets[].name`) are the attributes you can filter on with `fq`. Typical names: `category`, `brand`, `colors`, `style`, `material`, `season`, `gender`, `onSale`, `price`, `rating`. Look for a facet that names the topic directly, such as `sport`, `activity`, `occasion`, `pattern` or `collection`.
- **Existing dynamic categories** show the names the category builder uses. Fetch a few with `search_dynamic_categories` and `category_id`, and read `conditionConfig.rules[]`.
- **Product titles are not filterable.** `fq=title:"camo"` returns 0. A topic that lives only in titles has no rule yet (section 5).
- **`fq="field:*"` doesn't test whether a field is filled**; it matches every product.

**Check coverage before you trust an attribute.** Count the core products that carry the value: `fq` on the value plus `fq='pid:"A" OR pid:"B" …'` for up to 50 core IDs. If most core products lack it, the rule misses them. Report that as a data gap.

## 2. Fetching a rule's products

Call `search_discovery_product_grid_insights` one call at a time, with `fl="pid,title,brand"`.

| What the rule says | How to fetch it |
|---|---|
| One attribute, one or more values | `query="*"`, `fq='sport:"pickleball" OR sport:"paddle sports"'` |
| A category and one attribute | `search_by="category"`, `query="<category id>"`, `fq='sport:"pickleball"'` |
| Several conditions joined with AND | `query="*"`, `extra_params={"fq": ["category:\"20200\"", "sport:\"pickleball\""]}`. Each list item is its own `fq`, and the grid ANDs them. Each item can contain ORs. |
| A price cap | `extra_params={"fq": ["price:[* TO 100]"]}`. Numeric ranges work (`days_since_release:[0 TO 30]` was verified); check that `numFound` looks sensible. |
| A short list of products | `fq='pid:"A" OR pid:"B"'` |

- **Never put AND inside one `fq` string**: it returns 0, even when matching products exist.
- **Facet counts for a filtered field are unfiltered** (multi-select behaviour). Every other facet is filtered.
- **Colour facets count variants**, so totals can exceed `numFound`.
- `rows` up to 200 works; 500 returns HTTP 500. Use `start` to page.
- `list_categories` lower-cases category IDs. The grid needs `originalCategoryId`.
- To fetch an existing dynamic category, use `search_by="category"` with its `brg_dyn_…` ID. Its `category` facet lists other categories that share products, with counts: a cheap overlap check.

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

| Field | Values seen |
|---|---|
| `operator` (top level) | `AND`, `OR` (one operator joins all rules) |
| `level` | `PRODUCT`, `VARIANT` (colour was `VARIANT`) |
| rule `operator` | `ANY_MATCH`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN_OR_EQUAL` |

Facet and condition names don't always match: the facet `colors` is the condition attribute `color`, and the facet `category` is `category_id`. A category with `rules: []` and a list of product IDs is **manual** and never updates itself.

One top-level operator joins every condition, so a rule like "(category A OR category B) AND sport = pickleball" has to be written as one `category_id ANY_MATCH [A, B]` condition AND the sport condition. There is no NOT operator in the conditions seen; to keep a neighbour topic out, choose a narrower attribute rather than trying to exclude.

Write the rule in both forms:

- **Readable:** `sport = pickleball AND category IN (/sports/racket-sports, /sports/accessories)`
- **Dashboard conditions:** the `conditionConfig` shape above, with the condition attribute names.

## 4. Set-up steps for the Discovery dashboard

No Loomi Connect tool creates or edits dynamic categories (checked with `search_tools` in October 2026). Give the user these steps:

1. In the Discovery dashboard, open **Merchandising → Categories** (the dynamic category builder; the label can vary by account).
2. Create a dynamic category with the suggested name and the catalog shown in the grid response (`catalogName`).
3. Add each condition: attribute, operator, values, and product or variant level. Set the top-level match to AND or OR.
4. Save, wait for the sync, then check the product count matches the preview (within a few products; variant-level conditions can differ slightly).
5. Decide where it appears: the navigation tree (otherwise it has no path), a redirect from the topic's searches, or a landing page, email or recommendation feed.
6. Optional: add a category ranking rule to pin the top core products or bury the borderline ones.

## 5. When no rule is possible

- **Short term:** a manual collection of the core and likely product IDs, ordered by score. Say clearly that it **won't update itself**: new products need adding by hand.
- **Fix:** add or fill an attribute in the product feed (for example `sport = pickleball`). The `product-data-enhancer` skill can suggest values per product; the catalog owner makes the change.
- **Meanwhile:** redirect the topic's searches to the search results page of its best-converting wording, if that page is clean.
