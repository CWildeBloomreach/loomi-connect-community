# Business terms and how to map them

People ask questions in business words. This table maps the common ones to EQL, with the default to propose when the user doesn't say. **Always tell the user which definition you used.** Replace `purchase`, `total_price` and the other names with the project's own, from `get_event_schema` and `get_customer_property_schema`.

## Who

| Term | Default definition | EQL (inside `customers matching`) |
|---|---|---|
| Customer | Any profile that matches the conditions. Unique, not events. | `select count customers ...` |
| Buyer, purchaser | At least one order-level purchase in the period | `exists[event purchase in last 30 days]` |
| Active customer | Any session **or** purchase in the last 30 days. Ask: some teams mean "purchased in the last 90 or 365 days" | `exists[event session_start in last 30 days] or exists[event purchase in last 30 days]` |
| Visitor | Any session in the period | `exists[event session_start in last 30 days]` |
| New customer | First-ever purchase falls in the period | `exists[event purchase since <start>Z until <end>Z] and not exists[event purchase until <start>Z]` (pattern N in eql-patterns.md) |
| Returning customer | Bought in the period **and** before it | `exists[event purchase since <start>Z until <end>Z] and exists[event purchase until <start>Z]` (pattern N) |
| Repeat buyer (lifetime) | 2 or more purchases ever | `count event purchase >= 2` |
| Lapsed | Bought before, but not in the last N days. Ask N (90, 180 or 365 are typical) | `exists[event purchase] and not exists[event purchase in last 180 days]` |
| Subscribed / opted in | The project's consent category. Ask which. A boolean such as `email_opt_in` is **not** the same as consent | `has consent <category_id>`, or `customer.email_opt_in = true` labelled as "the opt-in property, not consent" |
| Contactable by email | Has an email address **and** consent. Never treat "has an email" as consent | `customer.email has value and has consent <category_id>` |

## What

| Term | Default definition | Notes |
|---|---|---|
| Order, purchase | One order-level purchase event | Not the item-level event, which counts line items |
| Items sold, units | Sum of quantity on the item-level event | Check the quantity property exists and is a number |
| Revenue, sales | Sum of the order value property on the order-level event | Ask: with or without tax, shipping, refunds. Split by currency |
| AOV (average order value) | Average order value on the order-level event | Weighted across rows, never an average of averages |
| Conversion rate | Customers who did step 2 within N days of step 1 ÷ customers who did step 1 | A funnel. State the window (default 7 days) |
| Purchase rate of visitors | Buyers ÷ visitors in the same period | Two customer counts, or a two-step funnel |
| Cart abandonment | Added to cart, no purchase within N days | Funnel `cart_update where .action = "add" followed by purchase`; check the action values |
| Top products / categories | Most frequent values of a property on the item-level purchase or view event | Use `grouping top 10`. Category values can differ between events |
| Top search terms | Most frequent values of the search term on the search event | Free text: show only the top values, never the long tail |
| Traffic source | `utm_source` / `utm_medium` on `session_start` | Not usually on purchase events |

## When

| Phrase | Default | EQL |
|---|---|---|
| "Last week", "last month" | The previous **calendar** week (Monday to Monday) or month, UTC | `since 2026-09-01T00:00:00Z until 2026-10-01T00:00:00Z` |
| "Past 7 / 30 days", "recently" | Rolling, ending now | `in last 7 days` |
| "This month so far" | From the 1st to now | `since 2026-10-01T00:00:00Z` (no `until`) |
| "Year to date" | From 1 January, UTC | `since 2026-01-01T00:00:00Z`. Long windows raise the cost |
| "Compared with last period" | The same length, immediately before | Run the same query twice: absolute dates, or `execution_time` moved back |
| "Last year" (same period) | Same dates one year earlier | Absolute dates |

**Time zones:** absolute dates with `Z` are UTC. Day and month breakdowns use the **project's** time zone, including daylight saving. Say which applies. If the user's business day is in another time zone and the answer is close to a boundary, mention it.

**"As of":** results are live. Always give the time the query ran. Recent data can still be arriving, so today's figures are usually incomplete.
