# Where Engagement A/B tests live, and how to count them

Every query here returns **aggregate counts**. None of them lists or reads individual customers.

Status labels:
- **Ran:** executed in live testing (October 2026, a sandbox project). Placeholder IDs were used, so this proves the syntax runs, not the numbers.
- **Parsed:** accepted by `estimate_eql_cost`, not executed. The cost shown is from a sandbox with about 370,000 customers; large production projects score higher.
- **From the docs:** taken from Bloomreach's documentation of system events; not checked live.

## The three kinds of test

| Test | Found with | Variants and split | Assignment is tracked as | Notes |
|---|---|---|---|---|
| **Web experiment** | `search_experiments` (list, then by `experiment_id`) | Detail lists the variants (control and treatments), traffic allocation and goals | `experiment` event: `experiment_id`, `experiment_name`, `variant_name`, `variant_id`, `action` (`show`, `click`, `close`, `submit`) (from the docs) | Can return HTTP 403; see below |
| **Scenario A/B split** | `search_scenarios`, then `search_scenario_nodes` (via `search_tools` and `call_tool`) | `ab-split` node: `variants` with `name` and `percentage`. Outputs start at `1` in variant order | `campaign` event with `action_type = "split"`: `campaign_id` (the scenario ID), `variant`, `variant_id` (from 0), `new_choice` (from the docs) | A split with no outgoing branches is often a holdout assigner |
| **Email campaign A/B test** | `search_email_campaigns` (list, then by `campaign_id`, without designs) | Detail includes the A/B split config and each variant | `campaign` events carry `variant` on every status (`delivered`, `clicked` and so on) | Automatic-winner tests send the winner to the rest after the test phase |

Web layers (banners) also run A/B tests, tracked on the `ab test` and `banner` events. They're outside this skill's scope unless the user asks; the same patterns work with `banner` and `banner_id`.

### Quirks

- `search_experiments` wraps its data in `{"result": {...}}`. It returned `success: false` with `[ACCESS_DENIED] ... (HTTP 403)` inside that wrapper on some projects, rather than an HTTP error, and an empty `data` list on others. Treat "403" as "not checked (no access)" and "empty" as "no web experiments", and say which.
- The experiment list has only names, status, tags and archived flag. Variants, traffic and goals appear only when fetched by ID.
- Experiment and campaign lists can include editors' names and email addresses. Never repeat them.
- Fetch email campaigns with `include_design=false` (the default). Never paste subject lines or body content beyond what the user needs to tell the variants apart.

## Step 1: find the variant names actually tracked (V)

The names in the definition and the names on events usually match, but check. This query is rated **high** (event breakdown), so run it only when the names are unclear and the user agrees.

```
select count event campaign where .action_type = "split" and .campaign_id = "<scenario id>" by event campaign.variant grouping top 10 with null since <start>Z until <end>Z
```

**Parsed** (high). For email, drop the `action_type` filter and add `and .status = "delivered"`. For web experiments, use `event experiment where .experiment_id = "<id>" and .action = "show"` and break down by `event experiment.variant_name`.

These are **event** counts. With `and .new_choice = true` added, a scenario split counts first assignments, which is close to unique customers.

## Step 2: customers per variant (A)

A `select` needs a `by` clause: break down by any low-cardinality customer property, include nulls, and **add up every row**. An empty `rows` list means 0.

**A1. Scenario split** (**Parsed**, medium):

```
select count customers by customer.<any property> grouping top 3 with null customers matching exists[event campaign where .action_type = "split" and .campaign_id = "<scenario id>" and .variant = "<variant>" since <start>Z until <end>Z] and not exists[event campaign where .action_type = "split" and .campaign_id = "<scenario id>" and .variant = "<other variant>"]
```

The `not exists` removes **mixed** customers (merged profiles that landed in both). With more than two variants, add one `not exists` per other variant. Count the mixed customers once with `exists[A] and exists[B]`.

**A2. Email campaign:** same shape, with `.campaign_id = "<campaign id>" and .status = "delivered" and .variant = "<variant>"` in place of the split filter. Not parsed separately.

**A3. Web experiment** (**Parsed**, medium):

```
select count customers by customer.<any property> grouping top 3 with null customers matching exists[event experiment where .experiment_id = "<id>" and .variant_name = "<variant>" and .action = "show" since <start>Z until <end>Z]
```

If the control group has no `experiment` events, the control can't be counted with EQL. Say so: a readout then compares treatments only, or relies on the experiment's own evaluation dashboard.

## Step 3: converters per variant (C)

**C1. Purchase after assignment, within an attribution window** (**Ran**, medium):

```
select count customers by customer.<any property> grouping top 3 with null customers matching funnel(campaign where .action_type = "split" and .campaign_id = "<scenario id>" and .variant = "<variant>" followed by purchase since <start>Z until <end>Z within 7 days)
```

- The inline `funnel(...)` takes no `end`. `since … until …` goes before `within`.
- `estimate_eql_cost` lists "lifetime date range" as a factor even with the window inside the funnel. Whether that window bounds both steps wasn't verified with real data. Cross-check one variant with C2; C1 should never be larger than C2.
- Use the attribution window the team uses (Bloomreach's automatic winner uses 4 hours for email; its evaluation guide uses 24 hours for web layers). Default to 7 days for scenarios and say so.
- For web experiments: `funnel(experiment where .experiment_id = "<id>" and .variant_name = "<variant>" and .action = "show" followed by purchase ...)`.

**C2. Purchased at any time in the test window** (**Parsed**, medium, same shape as A1):

```
... customers matching exists[<assignment filter> since <start>Z until <end>Z] and exists[event purchase since <start>Z until <end + attribution>Z]
```

Less precise (it counts purchases made before assignment), but simple and robust.

**C3. Clicks (email)**: `exists[event campaign where .campaign_id = "<id>" and .variant = "<variant>" and .status = "clicked" since <start>Z until <end>Z]`. Not parsed separately. Unique clickers ÷ unique delivered is the click rate.

## Step 4: revenue per variant (R), only for a revenue metric

**R1** (**Parsed**, **high**):

```
select sum event purchase.total_price by event purchase.<low-cardinality property> grouping top 5 with null customers matching funnel(<assignment filter> followed by purchase since <start>Z until <end>Z within 7 days) since <start>Z until <end + attribution>Z
```

- Rated **high**. Ask the user once before running revenue queries (one per variant).
- It sums **all** purchases those customers made in the window, not only the first one after assignment. Say so.
- Use the order-level purchase event, and check the value property in `get_event_schema`.

## Optional: lift by week (novelty check)

Repeat A and C1 with one-week windows (`since <week start>Z until <week end>Z`) for the first and the latest full week. That's 4 extra queries per variant pair. Ask first.

## Budget

A two-variant conversion readout needs about 5 queries (2 × A, 2 × C1, 1 mixed check), all medium. A revenue metric adds 2 high queries. Space EQL calls (estimates included) at least 3 seconds apart: the limit is about one query every 3 seconds across the whole Engagement instance.
