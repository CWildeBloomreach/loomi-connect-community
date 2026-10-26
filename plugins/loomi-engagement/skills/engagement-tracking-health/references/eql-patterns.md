# EQL patterns for tracking health

These patterns were tested with `estimate_eql_cost` and `execute_analytics_eql` against a real Engagement project. Every one is **aggregate only**: it returns counts, never individual customers.

Always call `estimate_eql_cost` first, then run the query. Wait about 3 seconds between EQL calls. The analytics engine allows roughly **one query every 3 seconds** per project, which is stricter than the general Engagement limit, and a faster call returns a "Too many requests" error.

## Event volume by event type

```
select count any event by any event type grouping top 50 in last 7 days
```

- Cost: **medium**. Without `grouping top 50` it rates **high**, because the breakdown is unbounded. Always keep `grouping top N`.
- Event types with no events in the window **don't appear in the rows at all**. Compare the rows with `get_event_schema` to find types that have gone silent.
- If the schema has more than 50 event types, raise N to the schema count, up to about 200.

### The previous period

Run the **same query** with `execute_analytics_eql`'s `execution_time` parameter set to a Unix timestamp 7 days ago. `in last 7 days` is then measured back from that moment, which gives the previous 7 days. This is cheaper than a time breakdown.

```
execution_time = now − 7 × 86400
```

### A longer baseline

```
select count any event by any event type grouping top 200 in last 90 days
```

Cost: medium. For an average earlier week, take away the last 7 days' count and divide by 83 ÷ 7 (about 11.9). A type with a healthy 90-day count but nothing in the last 7 days has **stopped**. A type with no events in 90 days is historical or abandoned.

### Avoid

- `by column any event timestamp format year month day`: rates **high** or **very high**, even with `grouping top N` on the event type. Use the `execution_time` approach instead.
- `format year week`: this is a parse error. Supported formats include `year month day` and `year month`.
- `select last ...` and `select max any event timestamp ...`: `last` is a parse error, and `max ... timestamp` rates **high**. Use the 90-day count instead.

## Property fill rate on an event

```
select count event view_item by event view_item.brand grouping top 10 with null in last 7 days
```

- `with null` adds a row whose header value is `null`: these are events where the property is missing.
- **Fill rate** = 1 − (null row + empty-string row) ÷ the sum of all rows, including the `other` row.
- Cost: rated **high** whatever the date range, because the estimator doesn't credit a short window. Keep the window to 7 days or less and run it only for the few properties that matter, such as product ID, price and category on product events, or the total price on purchases.
- The order inside `by` is: attribute, then `grouping`, then `format`, then `with null`.

## Property fill rate on customers

```
select count customers by customer.country grouping top 10 with null
```

- Cost: **high** on large projects ("lifetime date range"), because it scans every customer. Run at most two or three of these, and only when the user agrees.
- **Check for empty strings as well as nulls.** In testing, the empty-string row (`""`) was ten times bigger than the null row. Counting only nulls overstates the fill rate badly.
- The top values also show **drifting or misplaced values**, such as postal or region codes in a country field, which usually means columns were shifted in an import.

## Value drift on an event property

```
select count event cart_update by event cart_update.action grouping top 10 with null in last 7 days
```

Run it twice, once with `execution_time` set 7 days back, and compare the shares. A new value, a vanished value, or a sudden change in share (for example `add` vs `remove`) usually means a tracking change. Only use this on **low-cardinality** properties, such as an action, status, currency, language or device. Never break down by free-text, URL, email or ID properties: the values may contain personal data and the result is huge.

## Filtering events

```
select count event page_visit where .path contains "search" by event page_visit.device grouping top 5 with null in last 7 days
```

- The `where` clause goes **before** `by`, and uses the `.property` shorthand.
- Only `and` is allowed in `where`. `or`, `not`, `is null` and multiple `where`s fail.
- `contains` works on strings.

## Syntax reminders

- A `select` with no `by` clause can't be run. Always add a breakdown.
- Use `grouping top N`, not `top N`.
- `customers matching ...` goes after the `by` clause.
- **Date windows inside `exists[...]`:** put `in last N days` *inside* the brackets. A trailing `in last N days` after `customers matching exists[...]` does **not** limit which events count. In testing it returned the lifetime figure, and the estimator rated it "low", which is misleading.
