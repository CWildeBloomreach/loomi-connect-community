# Engagement experiment readout

Reads out A/B tests in a Bloomreach Engagement project: web experiments, A/B split nodes in scenarios, and A/B tested email campaigns. For each test it reports the variants, planned and actual traffic split, customers per variant, the primary metric (conversion, revenue or click), lift with a confidence interval, significance and the chance each variant beats the control. It checks whether the test has run long enough (sample size, whole weeks, planned end, novelty effects, peeking), then recommends **Call the winner**, **Keep running** (with roughly how long) or **Stop: inconclusive**, showing every assumption. It uses aggregate EQL counts only, and it never changes anything.

The Discovery counterpart is `discovery-experiment-readout`.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_experiments`, `search_scenarios`, `search_scenario_nodes` (via `call_tool`), `search_email_campaigns`, `get_event_schema`, `estimate_eql_cost`, `execute_analytics_eql`, optionally `search_reports`, `calculate_report`, `search_dashboards` |
| **Tested with** | Claude Code, read-only and partial: `search_experiments` run against two sandbox and two production projects (empty on two, HTTP 403 on two, so no live experiment was read out); the EQL patterns parsed with `estimate_eql_cost` on a sandbox, and the conversion funnel pattern executed with a placeholder ID (empty result). Scenario split and email A/B config reading follow `engagement-scenario-explainer` and the tool schemas but weren't run live here. `scripts/ab_stats.py` tested on illustrative data. Not run end to end, and not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "How's the A/B test in our welcome flow doing? Can we call it?"
- "Which variant of last week's newsletter won, and was it significant?"
- "List our running experiments and tell me which ones are ready to call."
- "How much longer do we need to run the cart abandonment holdout test?"

See [examples/illustrative-readout.md](examples/illustrative-readout.md) for an example output. Its names and numbers are invented.

## How it works

1. **Find the tests:** web experiments with `search_experiments`; `ab-split` nodes in scenarios via `search_scenario_nodes`; A/B config on email campaigns. Records the variants, planned split, control and goal.
2. **Count:** unique customers per variant (excluding customers merged across variants), converters within an attribution window, and revenue if needed, all as aggregate EQL counts from the `campaign` (split and email) and `experiment` events. [references/data-sources.md](references/data-sources.md) has every query and its tested status.
3. **Statistics:** two-proportion z-test, confidence intervals on absolute and relative lift, Bayesian chance to beat control, Bonferroni correction for several variants, sample ratio mismatch check, required sample size and days remaining, and a novelty check by week. See [references/statistics.md](references/statistics.md). [scripts/ab_stats.py](scripts/ab_stats.py) does the maths (standard library only, no network).
4. **Recommend:** call the winner, keep running (with how long) or stop as inconclusive, using a decision table that also weighs duration, planned end, peeking and guardrail metrics.

It hands off to `engagement-scenario-explainer` when the user wants to know what a scenario does around the split.

## Notes and limitations

- Loomi Connect has no Engagement A/B report tool, so the statistics are computed from aggregate counts. Revenue significance assumes a spread of order values (default: standard deviation equal to the mean), because EQL can't return per-customer variance. The assumption is stated in every readout.
- `search_experiments` can return `ACCESS_DENIED` (403) inside a `{"result": ...}` wrapper. The skill carries on with scenarios and email, and says web experiments weren't checked.
- Event names and properties (`experiment` with `variant_name`; `campaign` with `action_type = "split"` and `variant`) come from Bloomreach's system event documentation and weren't seen with live data in testing. If the control group of a web experiment tracks no events, it can't be counted with EQL.
- Revenue sums are rated "high" by `estimate_eql_cost`, so the skill asks before running them. Customer counts are "medium" on a mid-sized sandbox and may be higher on large projects.
- Automatic-winner tests in scenarios and email only give a fair comparison during their short test phase.
