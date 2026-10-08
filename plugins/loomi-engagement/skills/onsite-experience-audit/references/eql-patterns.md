# EQL patterns for on-site experience performance

Every query here is **aggregate only**. Estimate each with `estimate_eql_cost` first, run `high` only with the user's agreement, and never run `very_high`. EQL allows about one query every 3 seconds across the whole Engagement instance.

Status labels:
- **Ran:** executed in live testing (October 2026).
- **Parsed:** accepted by `estimate_eql_cost`, not executed.

## The banner event

Engagement web layers track a `banner` event. In testing, its properties included `action`, `banner_id`, `banner_name`, `banner_type`, `variant_id`, `variant_name`, `variant_origin`, `interaction` and `campaign_id`. Check the project's `get_event_schema` first: a sandbox had only `action`, `banner_id` and `variant_id`.

The usual `action` values are `show`, `click` and `close`, but **check them before relying on them**: in one project with banner events, `.action = "show"` matched nothing. If the standard values return nothing, ask the user how their web layers are tracked. Code-heavy web layers sometimes send their own custom event (with a `banner_id` property) instead of, or as well as, `banner`.

## Prefer customer counts (cheaper)

Event-level breakdowns of `banner` are expensive. Count **unique customers** per banner and action instead:

```
select count customers by customer.<any_property> grouping top 3 with null customers matching exists[event banner where .banner_id = "<id>" and .action = "show" in last 30 days]
```

- Shape **Ran** (with `.action = "show"` and a 365-day window; it returned no rows in that project). Rated `high` on a sandbox of about 31 million profiles.
- `where` comes **before** the window inside `exists[...]`, and only `and` is allowed in it.
- Add up every row (including `null`, `""` and `other`). An empty `rows` list means 0.
- For each banner: run `show`, `click` and optionally `close`. That's 2–3 queries per banner, so do it only for the **active** experiences, and ask before running more than about 10.

Click-through = clickers ÷ viewers. Close rate = closers ÷ viewers.

For an A/B test, add `and .variant_id = "<n>"` (or `.variant_name`) to compare variants.

## Event-level (only for one short window)

```
select count event banner by event banner.action grouping top 6 in last 7 days
```

- **Ran** on a production project, rated `high` (score 57). It returned no rows, although one banner was active: that web layer tracked a custom event instead.
- The same with `in last 90 days`: `very_high`. Don't run.
- A cross-tab `by row event banner.banner_id ... by column event banner.action ...`: `very_high` even over 30 days, even on a small sandbox. Don't run.
- A customer breakdown by `event banner.action`: `very_high`. Don't run.

Use the 7-day event query only as a quick "is anything being tracked at all?" check.

## Is anything tracked at all?

```
select count customers by customer.<any_property> grouping top 3 with null customers matching exists[event banner]
```

**Ran** (lifetime, rated `high`). Narrow it with `in last 30 days` inside the brackets for a recent check.

## Revenue influence (optional, with care)

Don't attribute revenue to a web layer from EQL alone. If the user asks, compare purchase rates of customers who **clicked** with those who only **saw** it, as a customer count with `exists[event purchase in last 30 days]` added, and label it "correlation, not lift". Only an A/B test with a control group measures lift.
