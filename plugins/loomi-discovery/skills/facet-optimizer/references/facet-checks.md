# Facet checks: evidence and changes

Facet actions, as the Discovery dashboard and the facet-rule tools name them:

| Action | Rule field | What shoppers see |
|---|---|---|
| **Boost** (boost and always show) | `boosted_facets` {facet: position} | the facet near the top, in the position given |
| **Bury** (bury and always show) | `buried_facets` {facet: position} | the facet at the end of the list |
| **Hide** (always hide) | `excluded_facets` [facet] | no facet |
| **Always show** | `always_included_facets` [facet] | the facet appears; the algorithm picks its position |
| **Rename / merge / range / value order** | `aliases_facets`, `value_configs_facets` | set in the dashboard: the API tools say they don't support these |

Rules exist at three scopes: **global** (every search and category page), **site search** (one or more queries) and **category** (one or more category IDs). A narrower rule's settings apply on top of the global rule: in testing, the dresses category rule's boosts set the order, while the global rule's always-show facets still appeared.

## Junk facets

| Finding | Evidence needed | Change | Effort / risk |
|---|---|---|---|
| **Empty facet** | no values on every page reviewed; check whether a rule forces it (`always_included_facets`) | Remove it from always-show. If it should have values (e.g. a colour group), raise it as a catalog data gap | Low / low |
| **Internal field shown** ("cluster" with values like "c18") | the name or values mean nothing to a shopper | **Hide** globally | Low / low |
| **Internal field facetable but not shown** (`margin`, `omni_score_*`, `large_image`) | listed as facetable by `list_facet_attributes` | **Hide** globally as a precaution, especially anything commercial like margin or cost. Ask whether it needs to be facetable at all | Low / low |
| **Unbucketed number** (rating with one value per product) | a `number` facet with more than about 15 distinct values | Configure **ranges** (e.g. "4 stars and up") in the dashboard. Until then, **bury** or **hide** it, and remove any boost | Low (hide) / medium (ranges) |
| **Placeholder value** (rating "1.0" on 30% of products) | one value covers far more products than its neighbours | Fix the feed (missing ratings shouldn't be 1.0). Until then, a rating filter misleads shoppers: **hide** it | Medium / low |
| **Too many text values** (brand with about 200 values) | more than about 30 values | Keep it, but don't boost it to position 1 on broad queries. Check that the front end offers search-within-facet or "show more". Boost brand only on brand-led pages | Low / low |
| **Single value** ("gender: female" on women's dresses; one brand) | one value, or one value on almost every result | **Remove** the boost or always-show **for that category**. It can stay globally | Low / low |

## Missing or buried useful facets

Use this as the starting point for apparel. Adapt it for other verticals (for example, for electronics: brand, price, key specs).

| Product type | Show, in this order | Usually hide or bury here |
|---|---|---|
| Bottoms (pants, jeans, trousers, skirts) | size, colour, price, fit or style, brand | rating (until bucketed), season |
| Dresses | size, colour, price, length or style, occasion | gender, brand (if one brand) |
| Tops and T-shirts | size, colour, price, sleeve or style, brand | gender (on a gendered category) |
| Mixed-gender queries ("pants", "jeans", "shoes") | **gender** first or second, then size, colour, price | — |
| Accessories, bags, jewellery | price, colour, material, brand | size |

| Finding | Evidence needed | Change | Effort / risk |
|---|---|---|---|
| **Missing facet the product type needs** | the attribute is in `list_facet_attributes` but not in the page's facets | **Always show**, or **boost** to a position, for that category or query group | Low / low |
| **Price missing** | no `price` facet in the response, even though a rule configures price ranges | **Always show** price globally. Check the ranges in the dashboard | Low / low |
| **Gender missing on a mixed query** | the category facet shows both men's and women's categories with large counts | **Boost** gender for those queries, as a search rule | Low / low |
| **Key facet buried** | size or colour appears below junk or empty facets | **Boost** it to position 1–3 for that product type | Low / low |
| **Low coverage** | the facet's values cover under about 20% of results (size on 52 of 1,170 jeans) | A catalog data fix: populate the attribute. A rule can't fix it | Medium / low |
| **Several attributes for one concept** (`sizes`, `product_size`, `sku_size`, `br_slicing_size`) | more than one facetable attribute for size or colour, used in different rules | Pick one per concept, use it in every rule, and hide the others | Low / medium |
| **No attribute exists** (fit only appears in titles: "Slim", "Skinny", "Tapered") | not in `list_facet_attributes` | A catalog data fix: add the attribute to the feed | High / low |

## Values to merge or tidy

All of these are set in the dashboard (facet value settings), or fixed in the feed. Don't merge category facet values: the same name in two branches ("Pants" under Men and Women) is two categories, so `scripts/facet_summary.py` doesn't check that facet for merges.

| Finding | Example | Change |
|---|---|---|
| Case, spacing or punctuation variants | "Pacific" and "Pacific "; "USPA " | Fix in the feed (trailing spaces). Meanwhile, merge the values |
| Spelling variants | "gray" (665) and "grey" (33); "Denium" | Merge into the common spelling |
| Near-synonyms that shoppers see as one | "navy" and "navy blue" | Merge, if the business agrees |
| Raw labels | "true" / "false" on an on-sale facet; "c18" | Rename the facet and values ("On sale": "Yes"), or hide it |
| Test, campaign or internal values in the category facet | "test_yellow_color_products", "marketing campaign XYZ", "Demo Dress Brands" | Exclude dynamic categories from the category facet, or rename them for shoppers. Ask who owns them before removing anything: some get real traffic as landing pages |

## Notes

- **Order in the response.** `facet_counts.facets` comes back in display order after the rules are applied. Use it to judge what's buried.
- **Long value lists may be cut off.** The brand facet stopped at about 200 values in testing. Don't add up a long list's counts to judge coverage.
- **Value merges that never fire.** A category rule may merge values that never occur on that page (a "Canvas" merge on a dresses category). Harmless, but a sign that rules were copied without review.
- **Audience-targeted rules** can make two rules on the same category look like duplicates in the lists. Fetch each with `get_facet_rule` and check `audiences` before calling them duplicates.
- **Prove it with a test.** Facet changes are low risk, but their effect on conversion is hard to predict. For high-traffic pages, suggest an A/B test.
