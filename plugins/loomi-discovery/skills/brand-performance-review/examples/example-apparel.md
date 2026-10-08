# Example: brand performance review (demo apparel account)

The account name has been changed to a placeholder. The figures come from a real read-only run against a Bloomreach demo account in October 2026. The demo account's traffic is partly synthetic, so treat the numbers as illustrative.

**Prompt:** "Give me a brand scorecard for the last 30 days: who should we push, who's underdelivering, and what should our buyers raise with suppliers?"

**Calls made (one at a time):** `get_discovery_brand_performance` (613 brands); `get_discovery_product_performance_table` (6,631 products); `get_discovery_products_overview` (30 and 7 days); `get_discovery_query_performance` (830 queries); the product grid for the top 10 queries (24 rows each); the product grid for "mens belt" and "jeans" (200 rows) and "scharf" (24 rows). Then `scripts/brand_scorecard.py --ignore "AND,Basics"` and `scripts/grid_positions.py`.

## Brand performance review: example_apparel (account level, no sites), last 30 days

**Headline:** Three high-converting men's brands (Calvin Klein, GANT, GAS) are under-exposed, Tommy Hilfiger's 25 men's belts are all off the first page for "mens belt", and 12 brands draw far more name searches than their range can satisfy.

613 brands; account revenue $31.0M (+55.6% on the previous 30 days), conversion 26.0%, RPV $30.51.
**Data warning:** the brand table's previous-period revenue ($11.1M) doesn't match the product table and the overview ($19.9M), so trends were rebuilt from the product table. The brand table showed Polo Ralph Lauren at +345%; the product table gives +133%.

### Brand scorecard (top 10 by revenue)

| Brand | Products | Revenue | Rev share | View share | Exposure index | Conversion | Shelf share | Change vs account | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Pacific (house brand) | 436 | $11.55M | 37.2% | 25.0% | 1.49 | 28.0% | 40.9% | +3% | Premium; already dominant |
| Pacific Style | 155 | $4.20M | 13.5% | 3.2% | 4.27 | 26.5% | 1.1% | −3% | Premium (AOV $492) |
| Adidas | 103 | $2.95M | 9.5% | 10.0% | 0.95 | 29.6% | 6.2% | −1% | In balance |
| Calvin Klein | 20 | $1.30M | 4.2% | 2.8% | 1.48 | 30.8% | 6.3% | −8% | **Under-exposed** |
| Lacoste | 1 | $0.50M | 1.6% | 1.3% | 1.26 | 33.8% | 0.0% | +5% | **Under-exposed** |
| Van Heusen | 157 | $0.41M | 1.3% | 1.5% | 0.89 | 22.0% | 1.1% | −4% | In balance |
| GAS | 11 | $0.32M | 1.0% | 0.7% | 1.41 | 30.7% | 2.7% | −15% | **Under-exposed** |
| Tommy Hilfiger | 50 | $0.30M | 1.0% | 1.1% | 0.89 | 24.4% | 2.1% | −4% | Buried on "mens belt" |
| ethnix | 1 | $0.28M | 0.9% | 0.6% | 1.59 | 30.1% | 0.4% | +4% | **Under-exposed** |
| Roadster | 404 | $0.23M | 0.7% | 2.4% | 0.31 | 21.8% | 0.5% | −6% | **Over-exposed** |

### Ranking opportunities

| Brand | Issue | Evidence | At stake (working) | Action | Hand-off |
|---|---|---|---|---|---|
| Calvin Klein | Under-exposed overall, but already fills 14 of the first 24 for "jeans" | Index 1.48, conversion 30.8% vs 26.0% | $48k (6,916 visits × 4.8 pts × $146.81) | Look at category pages and other queries before boosting further | `discovery-category-health` |
| Tommy Hilfiger | Buried on "mens belt" | 25 matching belts, none in the first 24 (best 36, median 103); "mens belt" converts 10.6% against 21.3% for "belt" | $26k for the query (5,361 visits × 10.7 pts × $46.11) | Boost test on "mens belt" | `discovery-experiment-setup` |
| GANT | Under-exposed and falling | Index 2.88, conversion 33.5%; its one jeans product is at **25** for "jeans", visits −33% vs the account | $54k behind trend | Test bringing it onto the first page | `discovery-experiment-setup` |
| GAS | Under-exposed | Index 1.41, conversion 30.7%; best jeans at **26** for "jeans" | $10k (1,529 × 4.7 pts × $140.53) | Include in the "jeans" test | `discovery-experiment-setup` |
| Roadster | Over-exposed | 404 products, 2.4% of views, 0.7% of revenue, conversion 21.8% | $15k (8,556 × 4.2 pts × $42.72) | Limit on the queries where it's prominent | `discovery-experiment-setup` |
| SUITLTD | Over-exposed and falling | Holds **6 of the first 24 for "suit"**, converts 21.4%, revenue 22% behind trend | $14k behind trend | Bury test on "suit"; boost the high-converting Parx and Peter England suits instead | `discovery-experiment-setup` |

### Brands buried on their main queries

| Brand | Query (sessions) | Matching products | In first 24 | Best / median position |
|---|---|---|---|---|
| Tommy Hilfiger | mens belt (5,399) | 25 | 0 | 36 / 103 |
| Pacific | mens belt (5,399) | 27 | 1 | 10 / 78 |
| GANT | jeans (21,758) | 1 | 0 | 25 / 25 |
| GAS | jeans (21,758) | 11 | 2 | 19 / 24 |

On "mens belt", United Colors of Benetton has 8 of the first 24 slots (index 0.29, conversion 20.0%).

### Brand-name searches

| Brand | Brand searches | Conversion (baseline 16.8%) | Products carried | What shoppers see | Action |
|---|---|---|---|---|---|
| SCHARF | 3,432 | 11.2% | 5 | "scharf" returns 5 products: 2 belts and 3 wallets (two with the same title) | **Supplier: extend the range** |
| Sweet Dreams | 2,122 (9 queries, all for shorts) | 7.0% | 4 | not checked | Supplier: range; check results with `discovery-query-diagnosis` |
| Carlton London | 1,420 | 6.8% | 6 | not checked | As above |
| Columbia | 1,311 | 10.0% | 4 | not checked | As above |
| Jewel Junction | 1,233 | 7.6% | 1 | not checked | As above |

### Rising and falling

- **Rising:** Polo Ralph Lauren +50% vs the account (1 product), Parx +40%, next +28%.
- **Falling:** GANT −28% (visits fell; conversion rose), SUITLTD −22%.

### Supplier talking points

- **Tommy Hilfiger:** "You have 25 men's belts with us, but none appears on the first page when shoppers search 'mens belt', which is searched 5,400 times a month. We'd like to test giving them more visibility."
- **SCHARF:** "Shoppers searched for SCHARF 3,400 times last month, but we carry only five of your products. Can we extend the range?"
- **Calvin Klein:** "Your products convert at 31% against our 26% average and earn 4.2% of revenue from 2.8% of views. Would you support more visibility with co-op funding?"
- **Roadster:** "Your 404 products get 2.4% of views but 0.7% of revenue. Can you help with content, pricing or promotions?"

### Next steps
1. **A/B test a boost for Tommy Hilfiger on "mens belt"** (`discovery-experiment-setup`).
2. **Test a "jeans" rule** that brings GANT and GAS onto the first page and limits any one brand's share of it.
3. **Take the SCHARF, Sweet Dreams and Columbia range gaps to the buyers.**
4. **Test burying SUITLTD on "suit"** in favour of the higher-converting suit brands.

**Caveats:** views are product page visits, not impressions. Pacific Style's high index comes from price, not conversion. Shelf share covers the top 10 queries (30% of search sessions). Brand-search matching excluded "AND" and "Basics". Revenue at stake is an upper bound for the period.
