# Example: dynamic category review (illustrative)

This example is illustrative. The account, category names, IDs and figures are invented, though the patterns are ones seen while testing the skill against a demo account.

**Prompt:** "Can you review our dynamic categories? I think some of our collection pages are broken or duplicated."

## Dynamic category review: example_apparel (account level), last 30 days

**Summary:** 14 dynamic categories; 11 with traffic (38% of category sessions). 4 to fix now, 4 to make robust, 3 to tidy.

| Category | Definition | Products | Sessions | Conversion | Bounce | Flags |
|---|---|---|---|---|---|---|
| Under $200 | price ≤ 200 | 6,912 | 27,300 | 15.2% | 34.0% | — |
| Summer Sale | category = sneakers AND gender = female | 3 | 6,900 | 10.8% | 63.1% | Near-empty; nothing on sale; poor performance; duplicates /shoes/sneakers (women's) |
| Weekend Deals | onSale = true | 1,420 | 6,400 | 17.9% | 31.0% | Single value |
| Back in Stock | rating ≥ 40 | 0 | 2,100 | 0.0% | 92.4% | Empty |
| Heritage | brand = Brand A | 16 | 6,300 | 21.0% | 27.0% | Near-empty; single value |
| Holiday Gifts 2025 | collection = holiday-2025 | 212 | 1,850 | 9.1% | 58.2% | Seasonal tag; poor performance |
| Influencer Picks | pid in 101, 102, … (38 IDs) | 31 | 1,200 | 16.4% | 33.0% | Hard-coded IDs (7 no longer in the catalog) |
| Spring Edit | season = spring | 640 | 980 | 14.8% | 36.5% | Seasonal tag |
| Weekend Offers | onSale = true AND price ≤ 500 | 1,395 | 410 | 16.0% | 35.2% | Overlaps Weekend Deals (98%) |
| test_yellow_products | color = yellow | 85 | 6,400 | 15.0% | 40.1% | Test name with traffic |
| … | | | | | | |

Dynamic medians (11 categories with 100+ sessions): conversion 15.2%, bounce 35.2%.

### Fix now
1. **Back in Stock** (brg_dyn_example01): empty. Evidence: its only condition is `rating ≥ 40`, but ratings in the catalog run 0–5; 2,100 sessions hit an empty page (92% bounce). Action: change the condition to a restock or stock attribute, or `rating ≥ 4`. Effort: low. Check by: the grid returns products.
2. **Summer Sale** (brg_dyn_example02): 3 products, none on sale, and it's October. Evidence: 6,900 sessions; conversion 10.8% against a 15.2% median; bounce 63% against 35%; the definition is just women's sneakers. Impact: up to about $34k over 30 days. Action: retire it and point its links to Weekend Deals, or redefine it as `onSale = true AND gender = female`. Effort: low. Check by: the grid shows on-sale products; bounce drops the following week.
3. **Holiday Gifts 2025** (brg_dyn_example03): last year's collection still live. Evidence: `collection = holiday-2025`; 1,850 sessions at 9.1% conversion. Action: replace with this year's collection tag, or retire it before the season starts. Effort: low.
4. **test_yellow_products** (brg_dyn_example04): a test category with 6,400 sessions. Action: find the campaign or navigation link that points to it; rename it and make it a real collection, or remove the link. Effort: low.

### Make robust
1. **Influencer Picks**: 38 hard-coded product IDs, 7 of them no longer in the catalog. Replace them with a tag in the feed (for example `collection = influencer-picks`) so replacements join automatically. Effort: medium.
2. **Heritage**: one brand value and 16 products, under one screen. It converts above the median, so it works; add a second condition (`OR collection = heritage`) or monitor the brand value in the feed. Effort: low.
3. **Weekend Deals and Weekend Offers**: 1,395 of 1,420 products shared (98%). Merge them into Weekend Deals and redirect the smaller page's links. Effort: low.
4. **Spring Edit**: relies on `season = spring`. Confirm the feed still tags spring products, and plan an end date. Effort: low.

### Tidy up
- 3 dynamic categories have no tracked traffic in 30 days, including a "Demo Brands Page". Retire them if nothing links to them.

**Overlaps:** Summer Sale ⊂ /shoes/sneakers (100% of its products); Weekend Deals ≈ Weekend Offers (98%). Under $200 shares most products with several static categories, which is expected for a price-capped collection.
**A/B tests:** none running.
**Next steps:** run `discovery-category-health` for ranking on Holiday Gifts 2025 once its definition is fixed; run `facet-optimizer` on Under $200, which has 6,900 products and relies on facets to be usable.
