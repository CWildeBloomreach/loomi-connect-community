# Example: facet review (demo apparel account)

The account name has been changed to a placeholder, and editors' names are left out. This example comes from a real, read-only run against a demo account. Its traffic is synthetic, but the facets, rules and attributes are real.

**Prompt:** "Review the filters on our top search and category pages. What should we change?"

## Facet review: example_apparel (account level, last 30 days)

**Headline:** Shoppers on the biggest pages get no price filter, no gender filter on mixed queries, and a size filter that comes last, while an empty facet, an internal "cluster" code and a 200-value rating list take up the space. Fixing the global rule and adding three product-type rules touches every page reviewed.

**Reviewed:** 5 pages: searches "pants" (27,280 sessions), "dress" (26,372), "jeans" (21,758); categories women > dresses (21200) and women > tops (20100, 10,249 sessions). 4 facet rules: 1 global, 0 search, 3 category. 44 facetable attributes. 15 calls.

What shoppers see, in order:

| Page | Results | Facets, in display order | Missing |
|---|---|---|---|
| "pants" | 2,680 (1,206 men's, 1,475 women's) | brand (~200 values), colours, category, *colour groups (empty)*, size, released, rating (~200 values), on sale, season, *cluster*, material, style | gender, price |
| "jeans" | 1,170 (391 men's, 779 women's) | brand, colours, category, *colour groups (empty)*, released, rating, on sale, season, *cluster*, material, style (1 value), **size (last; covers 52 of 1,170)** | gender, price, fit |
| "dress" | 43 | brand (1 value), colours, category, *colour groups (empty)*, released, material, rating (43 values), on sale, season, style, *cluster* | size, price, length |
| Category dresses (21200) | 43 | colours, **rating (boosted to #2)**, **gender (1 value, boosted to #3)**, brand (1 value), *colour groups (empty)*, category, ... | size, price |
| Category women's tops (20100) | 748 | brand (~180 values), colours (40 values), category, *colour groups (empty)*, size, released, rating, ... | price |

Women's tops converts at 9.6% with 61% bounce, against 18.0% and 25% for men's pants (10200). It has no category facet rule. The facets may not be the cause, but they are the cheapest thing to test.

### Global changes

| # | Action | Facet | Evidence | Pages affected |
|---|---|---|---|---|
| 1 | **Always show** | price | No page shows a price facet, although the global rule configures price ranges (0–100, 100–200, 200+) and `price` is facetable | all |
| 2 | **Hide** | cluster | Values are codes ("c18", "c69", up to about 50 of them); shown on every page | all |
| 3 | **Remove from always-show** | color_groups | Empty on all 5 pages; the global rule forces it, taking a slot above size | all |
| 4 | **Bury**, then **hide** until fixed | rating | Raw values, not buckets: 43 values for 43 dresses, about 200 on "pants". "1.0" covers 27% of pants, 30% of jeans and 37% of tops: a placeholder. Ranges need the dashboard; the placeholder needs a feed fix | all |
| 5 | **Hide** (precaution) | margin, omni_score_* (9 fields), large_image, days_since_release | Facetable but meaningless or commercially sensitive. Not shown today; one rule change could expose margin | all |
| 6 | **Stop boosting to #1** | brand | Boosted to position 1 globally. It has about 200 values on "pants" and a single value on "dress" | all |

### By product type

| Product type (pages) | Show and order | Hide or bury | Evidence |
|---|---|---|---|
| Mixed-gender bottoms ("pants", "jeans"; check "trouser" and "skinny jeans" next) | 1 gender, 2 size, 3 colours, 4 price, 5 brand | style on "jeans" (one value, "Casual") | Both genders in large numbers; `gender` is facetable but never shown; size is last on "jeans" |
| Dresses (search "dress", "black dress", "cocktail dress"; category 21200) | 1 size, 2 colours, 3 price, 4 style, 5 material | gender, brand (one value each) | The category rule boosts rating to #2 and a one-value gender to #3; no size facet at all |
| Women's tops (category 20100; search "tops") | 1 size, 2 colours, 3 price, 4 style (Casual, Designer), 5 brand | — | No category rule: brand with ~180 values comes first; size is 5th behind an empty facet. Suggest an A/B test: 10,249 sessions at 9.6% conversion |

### Values to merge or tidy (dashboard or feed)

- **colours:** "gray" (665) and "grey" (33) on "pants" → "grey" or "gray"; consider "navy" / "navy blue". The global rule already merges "cream" and "beige" into "Creamy", which is the only capitalised colour.
- **brand:** trailing spaces split brands: "Pacific" / "Pacific ", "High Star" / "High Star ", "USPA ", "Masculino ", "Mufti Men ". Fix in the feed.
- **material:** "Denium" (on a dress) → "Denim".
- **on sale:** shown as "true" / "false". Rename the facet "On sale" and the value "Yes", or keep it as a toggle.
- **category:** dynamic and test categories appear as filter values on search pages: "test_yellow_color_products", "Demo Dress Brands", "Brand Example", "marketing campaign XYZ", "Sale Demin~~~Buy 1 Get 1 Free". "Under $200" is the top value on "pants" (2,677 of 2,680), so it can't narrow anything. Some are real landing pages ("marketing campaign XYZ" had 15,781 category sessions), so ask the owner before removing any.

### Catalog data gaps (not fixable with rules)

- **size** on jeans: values on 52 of 1,170 products. Most jeans have no size in the feed.
- **size** on dresses: no size facet at all on the dress pages.
- **fit:** no attribute exists. Fit appears only in titles ("Slim", "Skinny", "Tapered").
- **Several size attributes** are facetable (`sizes`, `product_size`, `sku_size`, `br_slicing_size`). Pages show `product_size`, but an audience rule on category 90200 boosts `sizes`. Pick one.

### Existing rules to change

- **Global rule 1265864:** add `price` to always-show; remove `color_groups`; hide `cluster` and the internal fields; drop the brand boost or move it below size and colour.
- **Category rule 1468672 (dresses, 21200):** remove `rating` and `gender` from boosts and always-show; boost `product_size` (once dresses have sizes) and `price`. Its "Canvas" material merge never applies to dresses; remove it.
- **Category rules 1756976 and 1756977 (category 90200):** not duplicates. One targets a high-value audience (boosts `sizes`), the other a low-value audience (boosts `colors`), though both lists show `audienceName: null`. Check that `sizes` has values on that category.

**Next steps:**
1. Update the global rule (price, cluster, colour groups, rating), and check "pants" and "dress" in the product grid afterwards.
2. Add search rules for the mixed-gender bottoms queries (gender, size, colour, price), and fix the dresses category rule.
3. A/B test a women's tops category rule (size, colour, price, style first).
