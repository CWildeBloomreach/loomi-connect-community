# Win-back opportunity

Sizes the revenue at risk from lapsing and lapsed customers in a Bloomreach Engagement project. It counts purchasing customers by days since their last purchase and by order count, works out each group's historical value and the revenue at stake (showing every assumption), checks which groups existing win-back or re-engagement scenarios and campaigns already cover, and recommends a win-back programme by value tier. It uses aggregate EQL counts only, and it never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `get_event_schema`, `get_customer_property_schema`, `estimate_eql_cost`, `execute_analytics_eql`, `search_predictions`, `search_segmentations`, `search_aggregates`, `search_scenarios`, `search_scenario_nodes` (via `call_tool`), `search_email_campaigns`, `search_sms_campaigns`, optionally `get_campaign_calendar` |
| **Tested with** | Claude Code: every EQL pattern run live and read-only against a sandbox project (as-of dates shifted with `execution_time`, because it has no recent purchases) and one recency count against a production project; coverage checks (segmentations, scenarios, email campaigns) run against production metadata. Not yet run end to end as a single session, and not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "How much revenue are we losing to customers who've stopped buying?"
- "Size our win-back opportunity and tell me what we're not covering."
- "How many customers haven't bought in 6 months, and what are they worth?"
- "Do we have a re-engagement flow for lapsed customers? What should it look like?"

See [examples/illustrative-winback.md](examples/illustrative-winback.md) for an example output. Its names and numbers are illustrative.

## How it works

1. **Recency × frequency grid:** 16 aggregate EQL counts: 5 recency bands, the 2–3 and 4+ order tiers within each band, and one average-order-value query. [references/eql-patterns.md](references/eql-patterns.md) has every tested query and its cost.
2. **Value and revenue at stake:** AOV × orders, with tier midpoints and adjustable assumptions about retained order rates and win-back rates. See [references/revenue-at-stake.md](references/revenue-at-stake.md). [scripts/winback_calc.py](scripts/winback_calc.py) builds the table (standard library only, no network).
3. **Coverage:** finds win-back-like scenarios, campaigns and segments, reads their recency conditions, and marks each band covered, partly covered or uncovered.
4. **Programme:** timing, channels and offer depth by band and value tier, with holdouts and exclusions. See [references/programme-playbook.md](references/programme-playbook.md).

It hands off to `engagement-segment-builder` to build the audiences and to `campaign-planner` to plan the sends.

## Notes and limitations

- On large projects, every customer count is rated "high" by `estimate_eql_cost`. The skill asks once before running them. It never runs a `very_high` query: per-band value sums are `very_high`, so value is estimated as AOV × orders instead.
- EQL is limited to about one query every 3 seconds across the whole Engagement instance, so the grid takes 2–3 minutes and may hit "Too many requests" if others are querying too.
- Revenue at stake and recoverable revenue are estimates built on stated assumptions, not forecasts.
- `search_predictions` returned HTTP 403 in testing. The skill carries on without predictions when that happens.
- Coverage is judged from scenario and campaign definitions, not from send history.
