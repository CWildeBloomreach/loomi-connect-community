# Examples: ask your data (illustrative)

**These examples are illustrative.** The query shapes, cost levels and response handling come from live, read-only testing, but the project names and every number have been invented. Nothing was created or changed.

---

## 1. A simple count, with a clarifying question

**Prompt:** "How many new customers did we get last month?"

**Assistant (before querying):** Two quick checks: by "new customer", do you mean someone whose **first-ever purchase** was last month, or a newly created profile? And "last month" as September 1–30 (UTC)? If you're happy with both, I'll go ahead.

**User:** First purchase, yes. September is fine.

**Answer:** About **1,700 customers** made their first-ever purchase in September 2026. That's 71% of the roughly 2,400 customers who bought that month; the other 29% had bought before.

| Buyers in September | Customers | Share |
|---|---|---|
| New (first purchase) | 1,712 | 71% |
| Returning | 694 | 29% |
| **All buyers** | **2,406** | 100% |

**Queries run** (Example Store – SANDBOX, as of 2026-10-08 10:15 UTC, both cost: medium)

    select count customers by customer.loyalty_tier grouping top 3 with null customers matching exists[event purchase since 2026-09-01T00:00:00Z until 2026-10-01T00:00:00Z] and not exists[event purchase until 2026-09-01T00:00:00Z]

    funnel purchase since 2026-09-01T00:00:00Z until 2026-10-01T00:00:00Z end

**Assumptions**
- Period: 2026-09-01 00:00 to 2026-10-01 00:00 UTC.
- Purchase = the order-level `purchase` event, all statuses (cancelled orders included).
- New = no `purchase` event before September 1. If order history before the project's start wasn't imported, some "new" customers may be older customers.
- Returning = all buyers (the one-step funnel) minus new buyers.

**Next:** Want these first-time buyers as a segment for a second-purchase journey? `engagement-segment-builder` can build "first purchase in the last 30 days" for you.

---

## 2. A high-cost query: ask first

**Prompt:** "What was revenue by day for the last 30 days?"

**Assistant:** I'll use the order-level `purchase` event and its `total_price`, split by `local_currency` so currencies aren't mixed. The query is:

    select sum event purchase.total_price by row event purchase timestamp grouping top 31 format year month day by column event purchase.local_currency grouping top 3 in last 30 days

`estimate_eql_cost` rates it **very_high** (score 81: event-based metric, two breakdown dimensions, 30-day event scan), so I won't run it. Two cheaper options:

1. **Revenue by day, USD only**: filter to one currency and drop the column breakdown. Rated **high** (score 52). Shall I run that?
2. **Weekly totals**: four separate weekly sums, each rated **high**. Slower, but each is smaller.

**User:** Option 1.

**Answer:** Revenue in USD over the last 30 days was about **$412,000**, averaging $13,700 a day. The highest day was Saturday 26 September ($24,100); the lowest was Monday 14 September ($8,200). Today (8 October) is incomplete and isn't included in the average.

| Day | Revenue (USD) |
|---|---|
| 2026-09-26 | 24,100 |
| ... | ... |
| 2026-09-14 | 8,200 |

**Query run** (Example Store – PROD, as of 2026-10-08 10:22 UTC, cost: high, run with your agreement)

    select sum event purchase.total_price where .local_currency = "USD" by event purchase timestamp grouping top 31 format year month day in last 30 days

**Assumptions**
- Period: the 30 days ending 2026-10-08 10:22 UTC. Days are in the project's time zone (America/New_York).
- Revenue = `total_price` on `purchase` (including tax and shipping), USD orders only; EUR and GBP orders (about 6% of orders) are excluded.
- Days with no purchases would be missing from the result; there were none.

**Next:** If the dip on the 14th looks like a tracking gap rather than real demand, `engagement-tracking-health` can check the purchase event's volume and properties.
