# Brand scorecard guide

The rules, the maths and how to turn each finding into a ranking action or a supplier conversation. The defaults match `scripts/brand_scorecard.py`.

## Measures

| Measure | Formula | Read it as |
|---|---|---|
| Revenue share | brand revenue ÷ account revenue | How much the brand matters |
| View share | brand visits ÷ account visits | How much attention it gets (product page visits; there are no impressions) |
| Exposure index | revenue share ÷ view share (= brand RPV ÷ account RPV) | Above 1: earns more per view than average |
| Conversion index | brand conversion rate ÷ account conversion rate | Above 1: shoppers who look, buy more often |
| Shelf share | share of the first 24 slots on the top queries, weighted by sessions | What shoppers see first |
| Change vs account | revenue ÷ (previous revenue × (1 + account trend)) − 1 | Gaining or losing ground, not just growing |
| Brand searches | sessions of queries containing the brand name | Demand the brand brings by itself |

## Flags

Brands with fewer than 500 visits (`--min-visits`) aren't judged on exposure.

| Flag | Rule | Meaning |
|---|---|---|
| **Under-exposed** | exposure index ≥ 1.25 **and** conversion index ≥ 1.10 | Earns and converts above average but gets fewer views than its revenue justifies |
| **Over-exposed** | exposure index ≤ 0.75 **and** conversion index ≤ 0.85 | Takes more views than its revenue justifies, and converts below average |
| **Premium** | exposure index ≥ 1.25, conversion normal | High RPV from a high price. Not a ranking issue in itself |
| **Budget** | exposure index ≤ 0.75, conversion normal | Low RPV from a low price. Not a ranking issue in itself |
| **Rising / falling** | change vs account ≥ +20% / ≤ −20%, and previous revenue ≥ 0.1% of the account | Gaining or losing ground |
| **Brand search converts badly** | brand searches ≥ 200 sessions, conversion < 75% of the account's search conversion | Shoppers ask for the brand by name and leave |
| **Thin range** | brand searches ÷ products carried ≥ 100 | More demand than range |

The conversion check matters. Without it, every expensive brand looks under-exposed and every cheap one over-exposed.

## Revenue at stake

All figures are upper bounds for the period, not forecasts.

- **Under- or over-exposed:** move the brand half-way to parity. shift = visits × |exposure index − 1| ÷ 2. At stake = shift × |brand conversion − account conversion| × brand AOV. Valued on conversion, so price level alone adds nothing.
- **Falling:** previous revenue × (1 + account trend) − current revenue.
- **Brand search converts badly:** brand-search visits × (account search conversion − brand-search conversion) × brand-search AOV.
- **Buried on a query** (from the ranking check): query sessions × (general query conversion − this query's conversion) × query AOV, as in `discovery-query-diagnosis`, when the query converts well below its general version (for example "mens belt" against "belt").

## From finding to action

| Finding | Ranking action | Supplier conversation |
|---|---|---|
| Under-exposed, and buried on its main query (many matching products, none in the first 24) | Boost test on that query: `discovery-experiment-setup` | "You convert at 31% against 26% on average; we'd like to give you more visibility. Would you support it with co-op funding?" |
| Under-exposed, already prominent on top queries | Check category pages (`discovery-category-health`) and long-tail queries | As above |
| Over-exposed | Bury or limit its share of the first page on the queries where it is prominent: `discovery-experiment-setup` | "Your products get 2.4% of views but 0.7% of revenue, and convert below average. Can you help with content, price or promotions?" |
| Premium or budget | None by itself | Useful context: say the index comes from price |
| Rising | Make sure stock and ranking keep up | "Your sales grew 50% faster than the site's. Let's plan the next quarter together" |
| Falling, visits fell | Check where it ranks; `discovery-query-diagnosis` on its main query | "Your share of views fell. Here's what we're doing about it" |
| Falling, conversion fell | Not a ranking issue: price, stock, content | "Conversion fell from X to Y. Has price or availability changed?" |
| Brand search converts badly, thin range | None in search | "Shoppers searched for you 3,400 times and we carry 5 of your products. Can we extend the range?" |
| Brand search converts badly, wrong results | `discovery-query-diagnosis` on the brand query | — |
| One brand fills most of the first page | Consider a rule limiting a brand's share of the first page, if its conversion is not the best | "You have 14 of the first 24 slots for 'jeans'" (a fact a supplier will value) |

## Caveats to state

- Visits are product page visits, not impressions. A brand can be shown often and clicked rarely; the tools don't show that.
- Brand names in the brand table are matched to the product table and to search queries ignoring case and surrounding spaces. Brand names that are common words need `--ignore`.
- In testing, the brand table's previous-period values (30-day window) didn't match the product table or the overview, so trends come from the product table.
- Shelf share covers only the queries fetched (usually the top 10, about 30% of sessions on the demo account).
