# Example: synonym review on a demo apparel account

The account name has been changed to a placeholder, and synonym IDs and user names have been removed. The figures come from a real read-only run against a demo account.

**Prompt:** "Can you audit our search synonyms and tell me what's broken?"

## Synonym review: example_apparel (account level)

**Headline:** the biggest problem is a missing wording on the 10th-busiest query: "tshirt" has a one-way synonym that skips "t-shirt", so it finds less than half the T-shirt range. A two-way group fixes it.

**Inventory:** 33 user synonyms (15 enabled, 18 disabled); 34,248 Bloomreach-generated (newest 50 reviewed). Tested in the product grid: 2 top queries and the 8 dead-end queries.

### Fix first (affects live traffic)
| # | Synonym or query | Type / direction | Problem | Evidence | Sessions (30d) | Recommendation |
|---|---|---|---|---|---|---|
| 1 | tshirt → tee, tees, t shirt | BR Generated - Global, one-way | Misses "t-shirt", the catalog's main wording | "t-shirt" returns 65 products, "tshirt" 26. Conversion 11.4% vs ~21.4% baseline; bounce 60% vs ~26% | 20,853 | Add a two-way group: tshirt, t-shirt, t shirt, tee. Upper bound ~$90k/30d |
| 2 | capris (no working synonym) | User, no-op (capris → capris) | Returns 0 products | "cropped trousers" returns 200 relevant products | 929 | Replace the no-op with one-way capris → cropped trousers, cropped pants |

### Bad expansions
| # | Synonym | Type / direction | Problem | Fires? |
|---|---|---|---|---|
| 3 | straws → coffee stirrers, stir sticks | BR Generated - Global, one-way | "straw hat" reaches it through the lemma "straws". Not an apparel product | Yes, on "straw hat" (888 sessions, 0 results) |
| 4 | swim → bikini, tankini, bathing suit, swimwear, swimsuit | BR Generated - Global, one-way | Sends men's "swim trunks" to women's swimwear terms | Yes, on "swim trunks" (1,060 sessions). Harmless today because the catalog has no swimwear |
| 5 | black long sleeve shirt → "accessories that make a black dress really stand out at a wedding" | BR Generated - Site, one-way | Target is an unrelated sentence | **Listed, not applied**: it didn't fire in the product grid |
| 6 | bkye heans → abercrombie jeans | BR Generated - Site, one-way | Adds a brand the shopper didn't type | Not tested |

### Clean-up (low risk)
- **No-op synonyms (10 enabled):** swim trunks, sports bra, capris, cummerbund, flippers, straw hat, corset, tiara, crossbody bag and cricket sweater each map to themselves (plus "shorts → shorts", disabled). Every one of the 8 dead-end queries has one, and none shows up in the product grid's synonym output. They look like failed fixes.
- **Leftover test synonyms (10 disabled):** "furniture", "carburator", "gumboot", "air conditioner", "selenium" and others → "necklace, dress".
- **Off-catalog:** "whiteboard cleaner", "white-tail deer", "whitecaps" (some enabled). Harmless, but noise.
- **Conflicting pair:** "white zigzag → white zig zag" (enabled) and "white zig zag → white zigzag" (disabled). Replace them with one two-way group.

### Next steps
1. Add the two-way T-shirt group, and re-run the product grid for "tshirt" to confirm about 65 results.
2. Replace the 8 no-op synonyms: a real mapping where the catalog has the product (capris), and a redirect where it doesn't. The `discovery-zero-results-triage` skill classifies each one.
3. Delete the disabled test synonyms in one clean-up pass, after confirming each one.
