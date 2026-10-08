# Engagement report explainer

Explains an existing Bloomreach Engagement analysis to someone who has inherited the project: a dashboard, report, funnel, trend, segmentation or event segmentation. It says in plain English what the analysis measures, its exact definition (events, filters, date window, conversion window, grouping), the current numbers where they can be calculated and what they mean, and the caveats that make it easy to misread, such as a filter that leaves out a channel or a fixed date range that stopped updating months ago. For a dashboard it summarises each component in layout order. An audit mode flags stale, broken or misleading definitions. It never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_dashboards`, `search_reports`, `search_funnels`, `search_trends`, `search_segmentations`, `search_event_segmentations`, `calculate_report`, `search_customer_filters`, `search_aggregates`, `search_expressions`, `search_predictions`, optionally `get_event_schema`, `estimate_eql_cost`, `execute_analytics_eql`. All are listed directly; any that a client doesn't show can be found with `search_tools` and run with `call_tool` |
| **Tested with** | Claude Code: live, read-only calls against a sandbox project (list and fetch a dashboard and a report, `calculate_report` on one cached report, list funnels, trends and event segmentations, all empty in the sandbox) and against one production project's funnel metadata (list, and one funnel definition). No trend or event segmentation definition was available to test, no EQL was run, and the skill hasn't been run end to end as a single session. Not yet tested in an OpenAI client |
| **Maintainer** | Bloomreach |

## Example prompts

- "List our dashboards."
- "I've just inherited this project. What does the 'Weekly KPIs' dashboard actually show?"
- "Explain the 'Repeat purchase funnel'. What exactly counts as a conversion?"
- "What's the current number on the 'Email revenue 30D' report, and is it trustworthy?"
- "Audit our saved reports. Which ones are stale or broken?"

See [examples/explain-and-audit.md](examples/explain-and-audit.md) for illustrative output.

## How it works

1. **Find:** lists the matching analysis type and matches the user's wording to a name, asking when several match.
2. **Read:** fetches the definition by ID and resolves the expressions, aggregates, segmentations and customer filters it references. [references/definition-fields.md](references/definition-fields.md) explains each field.
3. **Numbers:** for saved reports, `calculate_report` reads Engagement's cached result. Funnels, trends and segmentations have no calculate tool, so the skill offers an aggregate EQL equivalent instead (cost-estimated first).
4. **Caveats and audit:** applies the checks in [references/caveats-and-audit.md](references/caveats-and-audit.md): stale fixed windows, switched-off date filters, missing conversion windows, silent exclusions, event counts named as customer counts, ratio denominators, archived or missing references.

For follow-up questions the saved analysis doesn't answer, it hands off to `ask-your-data`, and for deeper funnel analysis to `funnel-leak-finder`, if those skills are installed.

## Notes and limitations

- Dashboard KPI tiles (`metric` components) have no read tool, so their definitions and values are reported as "not verified".
- `calculate_report` returns cached results. If a report hasn't been opened in the UI recently, the result can be empty or stale; the skill says so rather than presenting zeros as fact. Results have no column headers: values are labelled from the metric order in the definition.
- The dashboard `components` list isn't in display order; the skill sorts by position and skips blank spacer text blocks.
- Responses include editors' names. The skill never repeats them, and summarises HTML components rather than pasting them.
- [scripts/analysis_summary.py](scripts/analysis_summary.py) (standard library, no network) outlines a saved dashboard in layout order, labels a saved `calculate_report` result with dates and metric names, and lists every date and conversion window in a definition with stale or switched-off ones flagged.
