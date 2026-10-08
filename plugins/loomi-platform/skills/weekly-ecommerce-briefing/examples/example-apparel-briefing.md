# Example: weekly briefing (demo apparel account)

This example comes from a real read-only run on 8 October 2026. The Discovery sections use a Bloomreach demo account, renamed `example_apparel`, and its real figures (its conversion rate of about 50% is much higher than a real store's). The Marketing section was run against an Engagement sandbox project in a real organisation, which had no campaign sends that week; its name is replaced with a placeholder.

**Prompt:** "Give me the Monday briefing for example_apparel, and include email from our sandbox project."

**Calls made (one at a time):** 6 KPI cards, 1 trend, 4 tables, 2 dead-end presets, 2 pixel checks, the catalog list and catalog jobs (Discovery: 17); the campaign calendar, 1 cost estimate and 1 EQL query (Engagement: 3).

---

## Weekly briefing: example_apparel (account level) + Sandbox project, 30 Sep to 6 Oct vs 23 to 29 Sep

**Headline:** Revenue fell 3.7% to $7.63M on 3% fewer visits; conversion held, mobile was softest (−5.5%), and "diamond" searches lost the most revenue.

| | Revenue | RPV | Conversion | AOV |
|---|---|---|---|---|
| Overall | $7.63M (−3.7%) | $73.71 (−0.8%) | 50.6% (+0.1 pt) | $145.75 (−0.9%) |
| Search | $3.80M (−3.2%) | $43.02 (−0.2%) | 34.8% (0.0 pt) | $123.76 (−0.2%) |
| Category | $2.95M (−3.1%) | $40.78 (−0.3%) | 31.5% (−0.1 pt) | $129.57 (−0.1%) |
| Other* | $0.87M (−8.1%) | — | — | — |
| Desktop | $4.60M (−3.9%) | $74.28 (−0.5%) | 50.9% (+0.2 pt) | $145.84 (−1.0%) |
| Mobile | $1.51M (−5.5%) | $72.92 (−3.0%) | 49.9% (−0.8 pt) | $146.16 (−1.5%) |
| Tablet | $1.52M (−1.4%) | $72.83 (+0.5%) | 50.2% (+0.4 pt) | $145.08 (−0.4%) |

*Overall minus search and category; approximate, because a visit can include both.

**Top searches:** diamond $392k · dress $200k · mens pants $149k · black dress $146k · bags $139k · jewelry $138k · suit $131k · pants $127k · cocktail dress $116k · skirt $116k
**Searches with issues** (vs typical: conversion 21.3%, bounce 26%):
- tshirt: conversion 11.5%, bounce 60%, on 5.2k sessions. Up to $22k → `discovery-query-diagnosis`
- sweatshirt: conversion 14.1%, bounce 46%. Up to $10k → `discovery-query-diagnosis`
- shirt women: conversion 9.8%, bounce 54%, revenue −28%. Up to $8k → `discovery-query-diagnosis`
- 8 dead-end searches (swim trunks, sports bra, capris, straw hat, cummerbund…): 1,811 sessions, no product views. Up to $45k → `discovery-zero-results-triage`

**Top categories:** pacific specials $134k · rings $130k · necklaces $130k · bracelets $128k · jewellery $117k · valentine premium jewels $103k · special collection $99k · under $200 $96k · marketing campaign xyz $67k · limite collection page $66k
**Categories with issues** (vs typical: conversion 17.0%, bounce 26%):
- bracelets: conversion 10.5%, bounce 63%. Up to $79k → `discovery-category-health`
- valentine premium jewels: conversion 10.0%, bounce 63%. Up to $72k
- products under $25, summer sale, activewear: the same pattern (bounce 58–64%, conversion 8–11%)
- *Five categories share about 63% bounce and 10% conversion, which suggests one page or template problem. Check them together.*

**Top movers**
- Queries: ↑ "shorts" (+10% vs search trend, 1.8k sessions), "camo pants" (+10%) · ↓ "womens shorts" (−10%), "collared shirt" (−7%, −$6.8k). Biggest revenue drop: "diamond" (−$34.9k)
- Categories: ↑ jewellery (+$11.8k, +11%), activewear (+$7.3k, +24%) · ↓ pacific specials (−$16.7k, visits flat), rings (−$14.6k)
- Products: ↑ Mini Dress with Silver Heart (+$17.1k; visits 450 → 845) · ↓ Short Sleeve Polo Tennis Dress (−$13.1k, −17%)
- Brands: ↑ Tommy Hilfiger (+$5.4k, +7%) · ↓ Pacific Style (−$73.1k, −6.7%), next (−$11.1k, −19%)

**Marketing (Sandbox project):** No campaign sends recorded this week (calendar and email campaign events are empty).

**Health:**
- RED (ongoing): search results page pixel flags 100% of 25.9k events in 24 h as `catalogs_required` (the page doesn't send the catalog name). Search page-view metrics may be incomplete.
- AMBER (ongoing): the daily product feed succeeds but warns "Feed data contains null values".
- Everything else GREEN: order, product, category and add-to-cart pixels steady; 8,183 products, last index today 00:08 UTC.

### 3 things to do this week
1. **Fix the search results page pixel** (add the `catalogs` parameter): 100% of search page views flagged for at least two weeks. → `data-feed-health`
2. **Diagnose "diamond" search**: −$35k, order value $354 → $341 while conversion held, so higher-priced pieces may be ranking lower. → `discovery-query-diagnosis`
3. **Check the "pacific specials" collection**: −$16.7k with flat visits; conversion 16.3% → 14.9%. → `discovery-category-health`

Want to know why revenue fell? Run `revenue-anomaly-explainer`: in this run it found that most of the drop came from an unusually strong comparison week.
