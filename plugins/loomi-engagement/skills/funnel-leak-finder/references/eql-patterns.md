# EQL patterns for funnel leaks

Every pattern here is **aggregate only**: it returns counts or averages, never individual customers. These build on the tested patterns in `engagement-tracking-health` and `engagement-segment-builder`.

Status labels:
- **Ran:** executed successfully against live Engagement projects in October 2026 (a small sandbox and a large production project).
- **Parsed:** accepted by `estimate_eql_cost`, not executed.

Always call `estimate_eql_cost` first. Wait 3–10 seconds between EQL calls (estimates included): the limit is about one query every 3 seconds **per Engagement instance**, shared with other users, so 429s happen even when you call slowly. `execute_analytics_eql` also returns its own `cost_estimate` and `cost_warning` in the response.

## Funnels

### F1. The overall funnel (Ran)

```
funnel view_item followed by cart_update where .action = "add" followed by purchase in last 30 days within 7 days end
```

- Response: `data.total.counts` is a list of **customer** counts, one per step, for customers who did the steps **in order**, each within the conversion window (`within`) of the previous step. `data.total.times` is the average seconds between steps; `-1` for the first step and where nobody converted.
- `in last N days` **must come before** `within N days`, and the query **must end with `end`**.
- Each step can have a `where` filter, with the `.property` shorthand and `and` only.
- Cost: rated **high** on every project tested, including a 7-day window on a large project, and a 30-day one on a small sandbox. It ran in seconds on both. Ask the user once before running the funnel set.
- No checkout event? Leave the step out. With one, insert `followed by checkout` between cart and purchase.

### F2. Funnel for one device, OS or browser (Ran)

```
funnel view_item where .device = "Other" followed by cart_update where .action = "add" followed by purchase in last 30 days within 7 days end
```

- **Funnels don't accept `by`.** `... within 7 days by event view_item.device grouping top 5 end` fails with "Unexpected token by, expected end". Run one funnel per value instead, filtering the first step.
- Get the values first with V1. In testing, `device` held device families (`iPhone`, `Android`, `Other`), and almost all traffic was `Other` (desktop and unrecognised devices). `os` or `browser` may split better.
- The value must match exactly, including case.

### F3. Purchasers in the window: a sanity check (Ran)

```
funnel purchase in last 30 days end
```

- A one-step funnel counts customers with at least one purchase in the window. Rated **medium**.
- Compare it with the last step of F1. In testing on a production project, the customers F1 found buying after a cart add were only a few percent of all purchasers in the same window, although the purchases were all marked as online. When the funnel's purchase step is a small fraction of all purchasers, **purchases aren't linked to the browsing identity** (for example orders tracked server-side under another ID, or imported). Don't report that as a checkout leak.

### F4. Funnel by traffic source (Parsed)

```
funnel session_start where .utm_source = "google" followed by view_item followed by cart_update where .action = "add" followed by purchase in last 30 days within 7 days end
```

- Source properties (`utm_source`, `utm_medium`, `source`, `referrer`) are usually on `session_start`, not on `view_item`. Check the schema.
- Get the top values with V1 on `session_start` first. Don't break down by `referrer` or full URLs: they're high-cardinality and can contain personal data.

## Values

### V1. Top values of a property on an event (Ran)

```
select count event view_item by event view_item.device grouping top 5 with null in last 30 days
```

- Rated **high** on every project because of the event-property breakdown, but cheap in practice for a short window. Keep `grouping top N`.
- Same shape for `cart_update.action` (in testing: `add` and `remove`, plus an empty `null` row).

### V2. Average cart value (Ran)

```
select avg event cart_update.total_price where .action = "add" by event cart_update.action grouping top 3 with null in last 30 days
```

- Read the `add` row. The other rows come back as `null` because of the `where`.
- `total_price` on `cart_update` is usually the **running cart total** at the time of the event. **Don't sum it**: a customer who adds three items contributes three growing totals, so the sum overstates the value in carts several times over.
- In testing, `price` on `cart_update` was empty (sum 0), so check that the field you use is filled.

### V3. Average order value (Ran)

```
select avg event purchase.total_price by event purchase.purchase_source_type grouping top 5 with null in last 7 days
```

- Use any low-cardinality property on `purchase` for the `by` (a `select` needs one). Weight rows by their counts if there are several.
- Use `purchase`, not `purchase_item` (one event per line item).

### V4. Cart value from customers who didn't buy (Ran, with a caveat)

```
select sum event cart_update.total_price where .action = "add" by event cart_update.action grouping top 3 with null customers matching not exists[event purchase in last 30 days] in last 30 days
```

- **Order matters:** `customers matching ...` goes **after** the `by` clause and **before** the trailing `in last N days`. Putting `customers matching` after `in last 30 days` fails with "Unexpected token customers".
- Ran, but the sum suffers from the running-total problem in V2. Prefer: abandoned carts (F1) × average cart value (V2).

## Recovery flow activity

### R1. Sends per scenario (Parsed, from `engagement-scenario-explainer`)

```
select count event campaign by event campaign.campaign_id grouping top 50 in last 30 days
```

- Rated **high** even for short windows on large projects. Run only if the estimate is `low` or `medium`, or the user agrees.
- Match `campaign_id` to the scenario `_id`. An active abandonment flow with no `campaign` events in 30 days isn't running.

## Syntax traps

- Funnels: `in last` before `within`; trailing `end`; no `by`; no `customers matching` on a top-level funnel (use `select ... customers matching funnel(A followed by B)` instead, which takes no `end`).
- `where` only joins conditions with `and`. No `or`, `not` or `is null` (use `has no value` in `customers matching`).
- A `select` needs a `by` clause to run.
- A trailing `in last N days` after `customers matching exists[...]` doesn't limit the `exists`: put the window inside the brackets.
- The estimator doesn't check event or property names. Check them against `get_event_schema` first.
- Empty results come back as empty `rows`, or as rows with `0` or `null` values. Treat all three as zero.
