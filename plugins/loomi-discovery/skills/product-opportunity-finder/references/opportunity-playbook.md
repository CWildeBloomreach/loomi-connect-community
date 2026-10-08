# Opportunity playbook

How each group is defined, what to do about it, how the revenue at stake is worked out, and which skill to hand off to. The defaults match `scripts/product_opportunities.py`.

## Baselines

Only products with at least 30 visits are judged (`--min-visits`). For those:

- **Typical product**: the median ATC rate, conversion rate (CR) and RPV across products. Medians, not account totals, so a few best sellers don't set the bar.
- **High visibility**: visits in the top 10% (`--high-pct 90`).
- **Low visibility**: visits in the bottom half (`--low-pct 50`).
- **Well below / above typical**: at least 15% from the median (`--gap 0.15`), **and** the product's 90% Wilson confidence interval for that rate excludes the median. The interval stops small products with noisy rates from being flagged.
- **Account trend**: total revenue ÷ total previous revenue − 1, from the same table.

## Groups

### Fix the product page

- **Rule:** high visibility, ATC rate well below typical.
- **Why:** shoppers reach the page and leave without adding to cart. Search did its job; the page didn't.
- **Check:** price against similar products, images, description, size or colour availability, stock, reviews, delivery promises.
- **At stake:** visits × (typical ATC rate − its ATC rate) × its orders per ATC × its AOV. Uses the typical orders-per-ATC if it has no ATCs.
- **Hand-off:** product content, pricing or buying team, with the product IDs. Not a search fix. If it is also deep in its query's results, nothing else is needed.

### Over-exposed

- **Rule:** high visibility, ATC normal, CR well below typical.
- **Why:** it takes valuable slots but sells less often than the product next to it.
- **Check first:** where it ranks on its main query. If it's near the top, it is a bury candidate. If it's deep in the results, the views come from a category, recommendations or a campaign; don't bury it in search.
- **At stake:** visits × (typical CR − its CR) × its AOV. This is what a typical product would have earned from the same visits.
- **Hand-off:** `discovery-experiment-setup` (bury test on the query or category). If ATC is normal but conversion low, also check price at checkout, delivery cost and stock.

### Hidden gems

- **Rule:** low visibility, at least 5 orders, CR well above typical.
- **Why:** it converts when people find it, but few do.
- **Check first:** where it ranks on its main query and category. Off the first page (below 24) makes it a boost candidate. Already on the first page means the low visibility comes from low demand; look at its category or merchandising instead.
- **At stake:** (target visits − visits) × CR halfway between its own and typical × its AOV. The target is the 75th percentile of visits (`--gem-target-pct`). Halving the conversion advantage allows for broader audiences converting less well.
- **Hand-off:** `discovery-experiment-setup` (boost test). Group gems of the same brand or type into one rule.

### Declining winners

- **Rule:** previous revenue in the top 10% (`--winner-pct`), and current revenue at least 20% below previous revenue × (1 + account trend) (`--decline`).
- **Driver:**
  - **visibility**: visits fell at least 10% behind the account's visit trend. Check ranking on its main query, and whether a rule, a new product or a competitor brand pushed it down.
  - **conversion**: CR fell at least 10%. Check price changes, stock and sizes, reviews, competitor pricing.
  - **both** or **order value or mix**: check the above, and discounts.
- **At stake:** previous revenue × (1 + account trend) − current revenue.
- **Hand-off:** visibility → `discovery-query-diagnosis` on its main query, then `discovery-experiment-setup` if a boost is wanted. Conversion → pricing, stock or product page team.
- **Note:** in a fast-growing period, a winner can grow in dollars and still be "declining". Show the unadjusted change too.

### Dead weight

- **Rule:** in the catalog but with no visits (missing from the performance table, or 0 visits).
- **Why:** it can't sell if nobody sees it. It can also clutter results.
- **Check:** is it new (released in the last few days)? Out of stock? Missing a title, category or image? Mis-categorised?
- **Action:** fix product data so it's findable; or bury it, or clear it with a promotion, or remove it from the feed.
- **At stake:** not estimated. Report the count.
- **Hand-off:** product data or buying team; `discovery-category-health` if many sit in one category.

## Caveats to state

- Estimates are **upper bounds** for the period, not forecasts. They assume the product's rates hold when its exposure changes.
- The product table has **no impressions** and doesn't say whether a visit came from search, a category page or recommendations.
- Thresholds are relative to this account. A very small account may need `--min-visits` lowered and `--gap` raised.
