# EQL patterns for win-back sizing

Every query here returns **aggregate counts**. None of them lists or reads individual customers.

Status labels:
- **Ran:** executed successfully in live testing (October 2026, a sandbox and a production project).
- **Parsed:** accepted by `estimate_eql_cost` but not executed.

Replace `purchase` and `total_price` with the project's own purchase event and order-value property from `get_event_schema`.

## Getting a total

A `select` needs a `by` clause to run. Break down by any low-cardinality customer property, include nulls, and **add up every row**, including the `null`, `""` and `{"type": "other"}` rows:

```
select count customers by customer.<any_property> grouping top 3 with null customers matching <conditions>
```

- The breakdown property doesn't need values; a property nobody has just returns one `null` row with the whole total. **(Ran)**
- **An empty `rows` list means 0.** **(Ran)**

## R. Recency band totals

Put each window **inside** the brackets of `exists[...]`. A trailing `in last N days` after `customers matching ...` doesn't limit the events: it silently returns the lifetime figure.

| Band | `customers matching ...` | Status |
|---|---|---|
| 0–30 days | `exists[event purchase in last 30 days]` | Ran |
| 31–90 days | `exists[event purchase in last 90 days] and not exists[event purchase in last 30 days]` | Ran |
| 91–180 days | `exists[event purchase in last 180 days] and not exists[event purchase in last 90 days]` | Ran |
| 181–365 days | `exists[event purchase in last 365 days] and not exists[event purchase in last 180 days]` | Ran (same shape) |
| 365+ days | `exists[event purchase] and not exists[event purchase in last 365 days]` | Ran |
| All buyers | `exists[event purchase]` | Ran |

The five bands should add up to "all buyers". Check this: it catches typos and overlapping windows.

To exclude cancelled orders, filter inside the brackets, with `where` **before** the window: `exists[event purchase where .purchase_status = "shipped" in last 90 days]`. Use the same filter in every band.

Absolute dates work too: `exists[event purchase since 2026-01-01T00:00:00Z until 2026-04-01T00:00:00Z]` **(Ran)**. Always add the `Z`.

## F. Frequency tiers within a band

Add a lifetime order-count condition to the band:

```
... customers matching <band conditions> and count event purchase between 2 and 3
... customers matching <band conditions> and count event purchase >= 4
```

- `count event purchase >= 2` **(Ran)**; the combined form `exists[... in last 180 days] and not exists[... in last 90 days] and count event purchase between 2 and 3` **(Ran)**.
- 1-order customers = band total − (2–3) − (4+). This saves 5 queries.
- `count event purchase` counts every purchase event. If the project tracks one event per **item**, use the order-level event, or the counts will be inflated.

## V. Average order value

```
select avg event purchase.total_price by event purchase.<currency_property> grouping top 3 with null in last 30 days
```

- **(Ran)**, rated `high` with a 30-day window. A 365-day window was `very_high` on a project with only about 6 million events, so keep it to 30 days.
- The `null` currency row comes back with a `null` value: ignore it. If there's more than one currency, report AOV per currency and don't add them up.
- If there were no purchases in the last 30 days (common on sandboxes), set `execution_time` to a Unix timestamp in a period that had purchases. `execution_time` **does** move `in last N days` windows, including those inside `exists[...]` **(Ran: an `exists[event purchase in last 91 days]` count with `execution_time` at a quarter's end matched the `since … until …` count for the same quarter exactly)**.
- Fallback: ask the user for their AOV.

## T. Lifetime value tiers (optional)

Customers whose lifetime spend passes a threshold:

```
... customers matching <band conditions> and sum event purchase.total_price >= 200
```

- `sum event purchase.total_price >= 200` on its own **(Ran)**, at the same `high` cost as a plain count. Combined with a band: **Parsed** shape, not run.
- Pick 2–3 thresholds from the business's AOV (for example 1×, 3× and 6× AOV) and subtract to get tiers.

## Avoid (rated `very_high` in testing; don't run)

- `select sum event purchase.total_price by customer.<x> ... customers matching <band>`: an event-based metric over a lifetime range. Use pattern F with AOV instead.
- `select avg event purchase.total_price ... in last 365 days` or `since <3 years ago>`.
- `select count event purchase by event purchase timestamp format year month`: unbounded timestamp breakdown, and it can exceed the result cell limit.

## Costs seen in testing (for setting expectations)

| Query | Sandbox (~31M profiles, ~6M events) | Production (~80M profiles, ~700M events) |
|---|---|---|
| R or F customer count | high (42) | high (45), ran in a few seconds |
| V, 30-day AOV | high (58) | not tested |
| Sum of value per band | very_high (87) | not tested |

The estimator rates customer scans as "lifetime date range" even when every window is inside `exists[...]`.

## Reading recency conditions in scenarios and segments

When you read a scenario's condition node or a segmentation's definition (step 7), recency usually looks like one of these in `customer_filter.filters[]`:

- `"type": "funnel_steps"` with a step of `"type": "purchase"` and a `date_filter` such as `{"enabled": true, "duration": {"count": 90, "units": "days"}}`: "purchased in the last 90 days". If the `formula` negates it (for example `!F0`), it's "has **not** purchased in the last 90 days".
- `"type": "attribute"` with an `aggregate` or `embedded_aggregate` (for example a sum of `total_price`, or the last purchase timestamp) and a constraint such as `in between` or `greater than`: a value or recency tier.
- A segmentation attribute (`"type": "segmentation"` with an `id`): look up that segmentation by ID.

Turn each into plain words ("not purchased in 90 days, purchased in 180 days") and map it to the bands. An audience that covers "more than 90 days" covers the 91–180, 181–365 and 365+ bands unless something else narrows it.
