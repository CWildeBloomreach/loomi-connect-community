# Example: product data audit (illustrative)

**Illustrative only.** The account, products, brands and numbers below are invented. The patterns (a shared "buy online" template, empty material fields with the material in the description, vague colour values, "grey" vs "gray") are the kinds of gaps found when the method was checked against a demo account.

**Prompt:** "How good is our product data for SEO and AI search? Where should we start?"

**Calls made (one at a time):** `list_discovery_sites`; the product grid for `*` with facets (catalog shape); `search_discovery_catalog_products` for one product (attribute names); `get_discovery_product_performance_table` (all rows, saved); `get_discovery_query_performance` (top 200 queries, saved); the product grid with a `pid` OR filter, 10 calls of 50 IDs for the top 500 products by revenue. Then `scripts/audit_products.py` on the saved files with `--jsonl audit_results.jsonl --markdown`.

## Product data audit: example_apparel (account level), top 500 products by revenue, last 30 days

**Headline:** Two in five of your top sellers share one keyword-stuffed description template and have no material attribute, although the material is often written in the description: fixing the feed for those 212 products touches $1.9M of last month's revenue.

500 products audited (top 500 by revenue; 6,400 in the catalog). Average score 58/100: good 61, fair 172, poor 267.

### Most common gaps

| Gap | Products | Share | Revenue on affected products | SEO / AEO / GEO impact | Fix |
|---|---|---|---|---|---|
| Boilerplate description (D2) | 212 | 42% | $1.94M | Duplicate text across pages; nothing for an AI answer to quote | Product-specific descriptions (enhancer) |
| Keyword-stuffed description (D4) | 212 | 42% | $1.94M | "Buy … online at best price" reads as spam to search engines and assistants | Same as above |
| Missing material (A1) | 248 | 50% | $2.31M | Can't answer "is it cotton?"; missing from comparisons | 96 are quick wins (A3x below); the rest need a person |
| Material only in the description (A3x) | 96 | 19% | $0.88M | As above | Copy into the attribute in the feed |
| Vague colour "multi" (A2) | 71 | 14% | $0.52M | Colour filters and AI answers can't use it | Specific colours, from images (enhancer) |
| No GTIN or MPN (S1) | 500 | 100% | $4.80M | Shopping listings and AI shopping can't match the product | Catalog-wide: add identifiers to the feed |
| Title says one colour, data another (A3) | 38 | 8% | $0.41M | Assistants may describe the wrong colour | Check each (enhancer flags conflicts) |

### Catalog-wide issues

- Inconsistent values: colour "gray" (640) vs "grey" (66); "navy blue" (780) vs "navy" (22); brand "Harbour Line " with a trailing space (61).
- Fields missing everywhere: GTIN/MPN, image alt text.
- Boilerplate: 212 products share "…, Trousers, Bottomwear, Apparel, Buy … Online, Buy Trousers at best price".
- Field misuse: skincare ingredients ("Vitamin C", "Retinol") in `material`; shade words ("light", "medium") in `colors`.

### Categories to fix first

| Category | Products | Avg score | Revenue | Top gaps |
|---|---|---|---|---|
| men/pants | 96 | 41 | $0.92M | boilerplate; keyword stuffing; missing material |
| men/suits | 54 | 44 | $0.71M | boilerplate; missing material; colour "multi" |
| women/jeans | 61 | 63 | $0.55M | material only in description; raw HTML |
| jewellery/necklaces | 22 | 52 | $0.31M | short titles with no product type; thin descriptions |

### Products to enhance first

| # | Product (ID) | Category | Score | Revenue (30 days) | Main gaps |
|---|---|---|---|---|---|
| 1 | Northwind Men Grey Melange Regular Fit Solid Joggers (EX-1001) | men/pants | 39 | $41,200 | boilerplate; keyword-stuffed; missing material; colour "multi" |
| 2 | Kestrel Men Blue Slim Fit Formal Suit (EX-1187) | men/suits | 41 | $38,900 | boilerplate; missing material; colour "multi" |
| 3 | Halo pendant (EX-2002) | jewellery/necklaces | 46 | $22,300 | title has no product type ("pendant" only), no brand; thin description |
| 4 | Fernhill Women Navy Wide Leg Trousers (EX-1310) | women/pants | 48 | $19,800 | title says navy, colour field says black; material only in description |

### Invisible products with poor data

14 products with no views have scores under 40; 9 of them have titles without a product type ("Divine", "Aurora"). Shoppers can't find them by what they are.

### Next steps

1. Quick feed fixes (catalog team): copy material from descriptions for 96 products; merge "grey"/"gray" and "navy"/"navy blue"; trim brand names; strip HTML.
2. Enhance: run `product-data-enhancer` on EX-1001, EX-1187, EX-2002, EX-1310 and the next 16 by priority (batch 1 of 12). Full list in `audit_results.jsonl`.
3. Needs a person: GTINs for the whole catalog; materials for the 152 products with none anywhere.

**Caveats:** top 500 by revenue only; fill rates from facets are approximate; text-only (images not opened); illustrative numbers.
