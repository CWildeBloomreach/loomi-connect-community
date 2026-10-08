# Example: product opportunities (demo apparel account)

The account name has been changed to a placeholder. The figures come from a real read-only run against a Bloomreach demo account in October 2026. The demo account's traffic is partly synthetic, so its rates are unusually even across products; treat the numbers as illustrative.

**Prompt:** "Which products should we boost, bury or fix? Show me where the money is."

**Calls made (one at a time):** `get_discovery_products_overview`; `get_discovery_product_performance_table` (one page of 7,000 rows, saved to a file); the product grid for `*` (catalog count); `get_discovery_query_performance` for "jeans"; the product grid for "jeans", "ring" (200 rows each) and "suit" (24 rows). Then `scripts/product_opportunities.py` and `scripts/grid_positions.py` on the saved files.

## Product opportunities: example_apparel (account level, no sites), last 30 days

**Headline:** Three top-selling jeans have lost about a third of their share of visits while the site grew 56%, and two of them now sit just off the first page for "jeans"; together with other slipping winners, that's up to $706k behind trend.

6,631 products in the report, the same as the catalog (6,631), so every product had views. Typical product: ATC 34.2%, conversion 22.1%, RPV $9.71. Account revenue +55.6% on the previous 30 days ($31.0M), on visits +57%.

### Fix the product page (2, up to $0.6k)

| Product | Brand | Visits | ATC (typical 34.2%) | Conversion | At stake (working) | Action | Hand-off |
|---|---|---|---|---|---|---|---|
| Red & blood red Tank Top (103354) | URBANIC | 227 | 28.2% | 14.5% | $297 (227 × 6.0 pts ATC × 0.52 orders/ATC × $42.18) | Check images, sizes and price | Product page team |
| Charcoal Grey Textured Slim Fit Formal Trouser (108325) | Pacific | 229 | 28.4% | 18.3% | $288 (229 × 5.8 pts × 0.65 × $33.40) | Check sizes and stock | Product page team |

Small in this account: add-to-cart rates are very even across products.

### Hidden gems (134, up to $103k)

| Product | Brand | Visits | Conversion (typical 22.1%) | Main query: position | At stake (working) | Action | Hand-off |
|---|---|---|---|---|---|---|---|
| Goldmaster de Pacific Style ring (110467) | Pacific Style | 46 | 34.8% | "ring": **74 of 211** | $6.1k ((100 − 46) × 28.4% × $398.44) | Boost on "ring" | `discovery-experiment-setup` |
| Peter England Navy Neo Slim Fit suit (109874) and 6 more Peter England, Parx, V Dot and Van Heusen suits | various | 45–54 each | 33–40% | "suit": none in the first 24 of 677 | $12.7k for the seven | One boost rule for these suits on "suit" | `discovery-experiment-setup` |

Formal suits (Parx, Peter England, V Dot, Van Heusen, Arrow, Raymond and others) make up 11 of the top 15 gems: all convert at 31–40%, none gets more than 61 visits a month, and none of the seven checked appears on the first page for "suit".

### Declining winners (82, up to $706k)

Drivers: conversion 45, both 23, visibility 14.

| Product | Revenue now (prev) | vs account trend | Driver | Main query: position | At stake (working) | Action | Hand-off |
|---|---|---|---|---|---|---|---|
| GANT Men Blue Straight Fit Jeans (107119) | $136.8k ($122.5k) | −28% | visibility: visits −33% vs trend; CR +7% | "jeans": **25** | $53.8k ($122,460 × 1.556 − $136,760) | Find out what displaced it; test a boost | `discovery-query-diagnosis`, then `discovery-experiment-setup` |
| GAS Men Black Slim Fit Jeans (107371) | $99.8k ($93.6k) | −31% | visibility: visits −35%; CR +4% | "jeans": **26** | $45.8k | As above | As above |
| Calvin Klein Jeans Men Blue Tapered Fit (107169) | $124.3k ($107.8k) | −26% | visibility: visits −32%; CR +7% | "jeans": 3 | $43.4k | Already near the top for "jeans"; check categories and other queries | `discovery-query-diagnosis` |
| Panthère de Pacific Style necklace (110688) | $41.3k ($47.9k) | −45% | both: visits −21%, CR −30% | — | $33.2k | Check price, stock and the product page first | Pricing / product page team |
| Étincelle de Pacific Style wedding band (110401) | $27.4k ($34.2k) | −49% | both: visits −32%, CR −25% | "ring": 172 of 211 | $25.9k | Check stock and price; it is near the bottom for "ring" | Product page team, then `discovery-experiment-setup` |

The three jeans still grew in dollars, but their conversion held or rose while their visits fell far behind the account. That's a visibility problem, not a product problem. Calvin Klein has 14 of the first 24 slots for "jeans".

### Over-exposed (13, up to $25k)

| Product | Visits | Conversion (typical 22.1%) | Where it ranks | At stake (working) | Action | Hand-off |
|---|---|---|---|---|---|---|
| Tank Française ring (110440) | 545 | 16.2% | "ring": 63 | $6.2k (545 × 6.0 pts × $193.00) | **Don't bury in search**: it's already deep. Its views come from a category or recommendations; find the source | `discovery-category-health` |
| Theme Black Woollen Tailored blazer (110079) | 445 | 15.7% | not checked | $5.0k (445 × 6.4 pts × $178.51) | Check its main query, then test a bury | `discovery-experiment-setup` |
| Louis Philippe White Formal Shirt (108968) | 888 | 13.7% | not checked | $4.2k (888 × 8.4 pts × $57.00) | As above | `discovery-experiment-setup` |

### Dead weight (0)

Every catalog product had at least 20 visits in the period, so there's nothing to clear.

### Next steps
1. **Run `discovery-query-diagnosis` on "jeans"**, then A/B test a rule that brings GANT and GAS back onto the first page and limits any one brand's share of it (`discovery-experiment-setup`). Up to $100k behind trend.
2. **Test a boost for the converting formal suits on "suit"** (`discovery-experiment-setup`). Up to $13k.
3. **Ask the jewellery buyer to check price and stock** on the Panthère necklaces and Étincelle bands, whose conversion fell by a quarter or more.
4. **Find where "Tank Française ring" gets its 545 visits** before burying anything.

**Caveats:** thresholds are the script defaults (30+ visits judged; top 10% = high visibility; 15% gap with a 90% confidence check). The demo data is partly synthetic. Figures are upper bounds for the period, not forecasts.
