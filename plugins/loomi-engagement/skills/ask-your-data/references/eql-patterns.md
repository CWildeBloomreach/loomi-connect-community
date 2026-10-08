# EQL pattern library

Tested EQL patterns for common analytics questions. Every pattern returns **aggregate results**; none lists or reads individual customers. Replace event and property names (`purchase`, `total_price`, `local_currency`, `session_start` …) with the project's own, from `get_event_schema` and `get_customer_property_schema`.

Status labels:
- **Ran:** executed in live, read-only testing (October 2026), in this skill or in another skill in this repo.
- **Parsed:** accepted by `estimate_eql_cost`, not executed.

Cost levels are from testing. On a small sandbox (about 370,000 customers, 2.7 million events) the same query is often a level lower than on a large production project. **Always estimate first**: never run `very_high`, and run `high` only with the user's agreement.

## Quick chooser

| Question shape | Pattern | Usual cost |
|---|---|---|
| How many customers did X (in a period)? | C1 / C2 | medium (small project), high (large) |
| How many purchasers? (cheapest) | F1 | medium |
| How many customers did X, by a customer attribute? | C3 | medium–high |
| How many events / orders? | E1 | high |
| Total or average of a value (revenue, AOV)? | S1 / S2 | high |
| Top N values of a property? | T1 | high |
| What share converted from A to B? | F2 / F3 | medium–high |
| Trend by day / month? | D1, or D2 (cheaper) | high |
| This period vs the previous one? | P1 | 2× the base query |
| New vs returning buyers? | N1 | medium |
| Repeat buyers? | R1 | high (lifetime) |

## Getting a single total from a report

A `select` without `by` can't be run. Break down by any low-cardinality customer property, include nulls, and **add up every row**:

```
select count customers by customer.<low_cardinality_property> grouping top 3 with null customers matching <conditions>
```

- If nobody has the property, the whole total comes back in one `null` row. **(Ran)**
- Add up `null`, `""` and `{"type": "other"}` rows too.
- An empty `rows` list means 0. **(Ran, in other skills)**

## C. Customer counts

**C1. Customers who did X in a rolling window (Ran, medium on a sandbox)**

```
select count customers by customer.<property> grouping top 3 with null customers matching exists[event purchase in last 30 days]
```

**C2. Customers who did X in a fixed period (Ran)**

```
... customers matching exists[event purchase since 2026-09-01T00:00:00Z until 2026-10-01T00:00:00Z]
```

**C3. Customers who did X, broken down by a customer attribute (Ran)**

```
select count customers by customer.country grouping top 10 with null customers matching exists[event purchase in last 30 days]
```

Pick an attribute from `get_customer_property_schema`. Check for big `null` and `""` rows.

**Conditions you can combine** inside `customers matching` with `and`, `or`, `not` and parentheses:

| Wording | EQL | Status |
|---|---|---|
| Did X with a property filter | `exists[event purchase where .total_price > 100 in last 30 days]` (`where` **before** the window) | Ran (other skills) |
| Did **not** do X | `not exists[event purchase in last 30 days]` | Ran (other skills) |
| Did X at least N times | `count event purchase in last 365 days >= 2` | Parsed (the lifetime form `count event purchase >= 2` ran) |
| Lifetime spend over a threshold | `sum event purchase.total_price >= 200` | Ran (other skills) |
| Customer property equals | `customer.country = "US"` | Parsed |
| Property has a value | `customer.email has value` / `has no value` | Parsed |
| Did X before a date | `exists[event purchase until 2026-09-01T00:00:00Z]` | Ran |
| Has consent | `has consent <category_id>` | Parsed |

## F. Funnels (often the cheapest way to count customers)

**F1. Purchasers in a window: one-step funnel (Ran, medium)**

```
funnel purchase in last 30 days end
```

- `data.total.counts[0]` is the number of unique customers with at least one purchase in the window.
- In testing it matched C1 exactly (same window, same event). Use one to cross-check the other.

**F2. Conversion from A to B (Ran, medium on a sandbox; high on large projects)**

```
funnel session_start followed by purchase since 2026-09-01T00:00:00Z until 2026-10-01T00:00:00Z within 7 days end
```

- `counts` = customers at each step, **in order**, each within the `within` window of the previous step. Conversion = `counts[1] ÷ counts[0]`.
- `times` = average seconds between steps (`-1` for the first).
- The date filter (`in last …` or `since … until …`) **must come before** `within`, and the query **must end with `end`**.

**F3. Funnel with step filters (Ran, in `funnel-leak-finder`)**

```
funnel view_item followed by cart_update where .action = "add" followed by purchase in last 30 days within 7 days end
```

- Funnels **reject `by`**. To split by device or source, run one funnel per value, filtering the first step (`view_item where .device = "iPhone"`).
- Funnels reject `customers matching`. For "customers who did A then B" as a condition, use `select count customers ... customers matching funnel(A followed by B)` (no `end`).
- If the last step is a small fraction of F1's purchasers, purchases may not be linked to the browsing identity. Say so rather than calling it a conversion problem.

## E. Event counts

**E1. Number of events, split by a low-cardinality property (Parsed, high on a sandbox)**

```
select count event purchase by event purchase.local_currency grouping top 5 with null in last 30 days
```

- Event counts are not unique customers: say so.
- Always bound the date range: a query with no range is `very_high`.

**E2. Volume of every event type (Ran, medium, in `engagement-tracking-health`)**

```
select count any event by any event type grouping top 50 in last 7 days
```

## S. Sums and averages

**S1. Revenue by currency (shape of S2 with `sum`; not run in testing, expect high)**

```
select sum event purchase.total_price by event purchase.local_currency grouping top 5 with null in last 30 days
```

- Never add up different currencies. Report each, or ask which to use.
- Use the **order-level** event. `total_price` on `cart_update` is a running cart total: never sum it.

**S2. Average order value (Ran, high, in other skills)**

```
select avg event purchase.total_price by event purchase.local_currency grouping top 3 with null in last 30 days
```

- The `null` row comes back with a `null` value: ignore it. If there are several rows, weight by order counts (E1) rather than averaging the averages.
- 365-day windows were `very_high` even on a small project. Keep to 30 days, or ask the user.

## T. Top values

**T1. Top N values of an event property (same shape as breakdowns that ran in `engagement-tracking-health` and `funnel-leak-finder`; expect high)**

```
select count event search by event search.search_term grouping top 10 in last 7 days
```

- Rows are sorted by header, not by count: sort them yourself.
- Keep N small (10–20) and the window short (7–30 days).
- Never break down by email, ID, IP, cookie, URL or other personal or very high-cardinality properties.
- Category values can differ between events (slugs on views, display names on purchases). Check before comparing.

**T2. Top values by unique customers** (cheaper on big projects): run C1 once per value with a `where` filter inside `exists[...]`. Only do this for 3–5 values.

## D. Trends over time

**D1. Daily counts (Parsed, high on a sandbox)**

```
select count event purchase by event purchase timestamp grouping top 31 format year month day in last 30 days
```

- Order inside `by`: attribute, `grouping`, `format`, `with null`. **(Parsed)**
- Use `by event purchase timestamp`, **not** `by event purchase.timestamp`: the dotted form looks for a property called `timestamp` and returns no rows.
- Without `grouping top N` it rates higher and can return thousands of rows.
- `format year week` does not parse; use `year month day` or `year month`.
- Daily buckets use the **project's** time zone, including daylight saving.
- Days with no events are missing from the rows: fill them with 0 yourself.
- Unbounded or long timestamp breakdowns (a year by day, all time by month) are `very_high` on large projects.

**D2. Cheaper trend: a few periods, one query each.** Run F1 or C2 once per week or month with absolute dates. Four to six medium queries are often better than one `very_high` breakdown. Ask before running more than six.

## P. Comparing periods

**P1. Same query, earlier period.** Either:

- use absolute dates for both periods (`since … until …`); **(Ran)** or
- run the identical rolling query with `execute_analytics_eql`'s `execution_time` set to a Unix timestamp N days earlier. It moves every `in last N days` window, including those inside `exists[...]`. **(Ran, in other skills)**

Report both values and the change as a percentage. With small numbers (under about 100), give the absolute change too and avoid strong claims.

## N. New vs returning buyers

**N1. New buyers in a period: first-ever purchase falls in the period (Ran, medium on a sandbox)**

```
select count customers by customer.<property> grouping top 3 with null customers matching exists[event purchase since 2026-09-01T00:00:00Z until 2026-10-01T00:00:00Z] and not exists[event purchase until 2026-09-01T00:00:00Z]
```

- `until` on its own (no `since`) works inside `exists[...]`.
- **Returning buyers** = the same with `exists[...]` instead of `not exists[...]` for the earlier purchase. **(Parsed shape)** Or: all buyers in the period (C2) minus new buyers.
- New buyers can't exceed all buyers in the period (C2). Check it.
- Imported history matters: if purchases before a date weren't imported, everyone looks new. Ask when data starts if the share looks too high.

## R. Repeat buyers

**R1. Customers with 2+ purchases ever (Ran, high, in other skills)**

```
select count customers by customer.<property> grouping top 3 with null customers matching count event purchase >= 2
```

Repeat rate = R1 ÷ all buyers (`exists[event purchase]`). Both are lifetime scans, so both are usually `high` on large projects.

## Syntax traps (all confirmed in testing)

- A `select` with no `by` is not executable. Add a breakdown.
- `grouping top N`, not `top N`.
- `customers matching` goes **after** `by`, and **before** a trailing `in last …`.
- A trailing `in last N days` after `customers matching exists[...]` doesn't limit the `exists`: you get a lifetime figure. Put the window **inside** the brackets.
- Inside `exists[...]`, `where` comes **before** the window.
- Event filters use the `.property` shorthand: `where .total_price > 100`.
- `where` joins conditions with `and` only. No `or`, `not`, `is null` (use `has no value` in `customers matching`).
- `is in ["a", "b"]` takes strings only, and at least two.
- Quote hyphenated names: `customer."clarity-test"`, `."user-agent"`.
- `since … until …` with `Z`. `from … to …` doesn't parse. ISO dates without `Z` are read as UTC anyway, but be explicit.
- Funnels: date filter before `within`; trailing `end`; no `by`; no `customers matching`.
- The estimator **doesn't check names**. Check every event and property against the schema first.
- Zero can come back as empty `rows`, a `0`, or a `null` value.
