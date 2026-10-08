# Classification guide

How `scripts/new_arrivals.py` sorts new products, what to do about each group, how the revenue at stake is worked out, and where to hand off. Read this in steps 6, 8 and 9 of the skill. The method follows `product-opportunity-finder` (medians, Wilson intervals, revenue working), adjusted for products that haven't been live for the whole window.

## Baselines

- **Typical product**: the median of **established** products (not new) with at least 30 visits (`--min-visits`): visits per day, ATC rate, conversion rate (CR) and RPV. Medians, so a few best sellers don't set the bar. Established products, so a big launch doesn't move its own benchmark.
- **Days live**: a new product's age + 1 − the reporting lag (`--lag 2`, because dashboard data usually ends about 2 days before today), capped at the window. A product released after the report's last day has no data yet: **too early**.
- **Exposure index**: the product's visits per day live ÷ the typical product's visits per day. 1.0 = seen as much as a typical product. This is the age adjustment: a 5-day-old product with 50 visits is seen at a 30-day product's rate of 300.
- **Well below / above typical**: at least 15% from the median (`--gap`), **and** the product's 90% Wilson interval for the rate excludes the median.
- **Release ages ignored** when the release data check fails (most "new" products had views before their release date) or with `--no-age`. Every product is then judged on the whole window.

## Groups (checked in this order)

### Invisible

- **Rule:** no visits, not in the product table at all, or an exposure index below 0.1 (`--invisible`).
- **Why it matters:** shoppers can't buy what they can't find.
- **Check:** is it in a category (`search_discovery_catalog_products`, `category_paths`)? Does its own title return it in the grid? Is it in stock and flagged available? Is it excluded by a rule? Is it in the grid at all (`search_by="product_id"`)?
- **Action:** fix the data or categorisation. If it's simply new, give it a week.
- **Hand-off:** catalog owner and `data-feed-health`; `discovery-category-health` if many sit in one category.

### Too early

- **Rule:** fewer than 30 visits but not invisible, or released after the report's last day.
- **Action:** re-check next week. Report the count, not each product.

### Slow start

- **Rule:** exposure index at least 0.5 (`--seen`) **and** ATC or conversion well below typical.
- **Why it matters:** shoppers find it and don't buy. Search did its job; the product page or offer didn't.
- **Check:** price against similar products, images, description, size and colour availability, stock, delivery promise, reviews. Low ATC points at the page or price; normal ATC with low conversion points at checkout, stock or delivery cost.
- **At stake:** visits × (typical CR − its CR) × its AOV.
- **Hand-off:** product content, pricing or buying team. If it ranks near the top of a busy page, consider moving it down until it's fixed (`discovery-experiment-setup`).

### Buried

- **Rule:** conversion well above typical **and** either an exposure index below 1 or (with `--positions`) a rank below 24 on its category or main query.
- **Why it matters:** it sells when people find it, but few do.
- **Check:** where it ranks (step 8). Off the first page: a boost candidate. Already on the first page: low demand for its type, so promote it outside search.
- **At stake:** (typical visits per day × days live − its visits) × a CR halfway between its own and typical × its AOV. Halving the conversion advantage allows for broader audiences converting less well.
- **Hand-off:** `discovery-experiment-setup` for a boost test. Group products of the same type or brand under one rule.

### Breakout

- **Rule:** exposure index at least 1, conversion not below typical, **and** either conversion well above typical or revenue per day live in the top 10% of established products.
- **Why it matters:** early winners sell out and deserve more exposure while demand is fresh.
- **Check:** where it ranks (protect it if it's on the first page), stock depth (orders per day × lead time), sizes and colours left.
- **Action:** promote (homepage, new-arrivals collection, email) and tell buying to check stock.
- **Hand-off:** `search-demand-to-campaign` for email or SMS, `collection-suggester` for a collection, buying team for stock.

### On track

Everything else: seen and converting within the normal range. Report the count only.

## The group comparison

| Measure | Meaning |
|---|---|
| Share of products | new arrivals ÷ all products (including new products missing from the table) |
| Share of views | new arrivals' visits ÷ all visits |
| Share of views, previous period | should be near 0 for products released in the window. If it equals the current share, the release data doesn't match traffic |
| Visibility index | share of views ÷ share of products. Below about 0.7: new products are under-exposed as a group |
| Age-adjusted index | the visibility index ÷ (average days live ÷ window). Only when release ages are trustworthy |
| ATC, conversion, RPV | new arrivals against the rest. Lower conversion with normal visibility points at range or price; normal conversion with low visibility points at placement |

## Placement on a page (`scripts/new_in_grid.py`)

- **Share of results**: new products among all matches (from the release facet, with facets on; otherwise from the rows fetched).
- **Share of top**: new products among the first 24.
- **Placement index**: share of top ÷ share of results. About 1: new products placed in proportion. Below about 0.7: pushed down; check the ranking algorithm and rules (a sales- or popularity-based ranking needs time to learn new products) and consider a "new" boost on that page. On the demo account: /men/suits 0.70 (30% of the range, 21% of the first page), "suit" 0.63, /women/dresses 0.94.

## Revenue at stake

Always show the working, and present it as an **upper bound for the period, not a forecast**. It assumes the product's rates hold when its exposure changes, which is optimistic for niche products.

## Thresholds to change

| Option | Default | Change when |
|---|---|---|
| `--days` | 30 | the user asks about a week (7) or a season (90) |
| `--min-visits` | 30 | a small account: lower it to 10–15 and say so |
| `--gap` | 0.15 | too many or too few flags; raise it on noisy accounts |
| `--seen` | 0.5 | slow starts should only count products seen at typical rates (1.0) |
| `--invisible` | 0.1 | fewer or more products should count as invisible |
| `--lag` | 2 | the dashboard data ends on a different day (check `get_discovery_trend`) |

## Caveats to state

- The product table has **no impressions** and doesn't say whether a visit came from search, a category page, recommendations or a campaign. A breakout may be riding an email; check before calling it organic.
- New products often rank low at first under ranking that learns from sales or clicks. A low position in week one isn't yet a problem; in week three it is.
- Account-level reporting (no sites) mixes every storefront.
