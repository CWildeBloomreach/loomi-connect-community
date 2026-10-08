# Example: dead-end searches on a demo apparel account

The account name has been changed to a placeholder, and rule and synonym IDs have been removed. The figures come from a real read-only run against a demo account. The revenue estimates use the account's top-query medians (about 21.4% conversion and about $118.90 average order value, so about $25.40 per session) and are upper bounds.

**Prompt:** "Which of our searches are dead ends, and what should we fix first?"

## Zero-results triage: example_apparel (account level, last 30 days)

**Headline:** 8 dead-end queries with about 7,370 sessions in total, and every one is growing 45–77%. All 8 show 0 product views and 100% bounce. 7 return **0 results**, and "sports bra" returns 1 off-target product.

**Pattern found:** each of the 8 queries has its own search-settings rule (exact match) that switches to text-match precision and turns **off** query relaxation and spelling correction, while the global rule has both on. Each query also has a user synonym that maps it to itself (for example "corset → corset"), which does nothing.

| # | Query | Sessions (change) | What shoppers get | Class | Fix | At stake (upper bound) |
|---|---|---|---|---|---|---|
| 1 | capris | 929 (+77%) | 0 results | Synonym fix | One-way synonym capris → cropped trousers ("cropped trousers" returns 200 relevant products) | ~$23.6k |
| 2 | swim trunks | 1,060 (+53%) | 0 results. With the rule off, spelling correction rewrites it to "slim trends" and shows trousers | Catalog gap | Redirect to men's shorts or activewear; raise swimwear as a gap ("swimwear" returns only shorts and dresses) | ~$26.9k, partly recoverable |
| 3 | sports bra | 950 (+69%) | 1 result: a seamless sports top | Catalog gap (thin) | Redirect to women's activewear; raise as a gap | ~$24.1k, partly recoverable |
| 4 | cummerbund | 926 (+61%) | 0 results | Redirect candidate | Redirect to men's suits | ~$23.5k, partly recoverable |
| 5 | flippers | 922 (+57%) | 0 results. "flip flops" returns 1 false positive (shorts with a flip-flop print) | Catalog gap | Redirect to shoes; raise as a gap | ~$23.4k, partly recoverable |
| 6 | straw hat | 888 (+60%) | 0 results. A Bloomreach-generated synonym also expands "straws" to "coffee stirrers" | Catalog gap | Redirect to accessories; review the bad synonym | ~$22.6k, partly recoverable |
| 7 | corset | 879 (+55%) | 0 results | Catalog gap | Redirect to women's tops; raise as a gap | ~$22.3k, partly recoverable |
| 8 | tiara | 820 (+45%) | 0 results | Catalog gap | Redirect to jewelry | ~$20.8k, partly recoverable |

**Existing fixes that don't work:** 8 self-referencing user synonyms ("tiara → tiara" and so on). No redirects cover any of these queries.

**Noise (no action):** about 20 queries with fewer than 30 sessions each, for example "handbga" (9 sessions) and "i need new hiking shoes" (1). Two no-sale queries sit above the threshold: "crop sleeveless crop top" (33 sessions, 15 product views, 3 add-to-cart) and "forever new midi skirt" (117 sessions, 35 product views, 6 add-to-cart, 0 orders). They aren't dead ends, because shoppers do click. Each is worth a `discovery-query-diagnosis` run.

### Next steps
1. **Review the 8 query-level search-settings rules.** They make each query stricter than the rest of the site. Preview each query in the product grid with its rule disabled before changing anything.
2. **Add the capris synonym**, the only query where the catalog clearly has the product.
3. **Add redirects** for the other 7, and send the list of gaps, with sessions and growth, to merchandising.
