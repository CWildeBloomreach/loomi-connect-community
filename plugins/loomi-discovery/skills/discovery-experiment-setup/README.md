# Discovery experiment setup

Guides the setup of a Bloomreach Discovery A/B test for a ranking rule, so the change is measured before it goes live for everyone. It checks for running tests and conflicting rules, looks at the query's traffic and live results, drafts the rule, previews its effect, estimates how long the test must run, and shows the full plan. It then creates the rule (disabled) and the experiment (draft), and starts the test, each only after its own explicit "yes".

| | |
|---|---|
| **Products** | Discovery |
| **Access** | **Writes**: creates a ranking rule (disabled), creates an experiment (draft), and starts the experiment. Each write needs explicit confirmation. Starting a test is live immediately |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `search_discovery_experiments`, `list_site_search_ranking_rules`, `list_category_ranking_rules`, `list_ranking_rules_global`, `get_ranking_rule`, `get_discovery_query_performance`, `get_discovery_category_performance_table`, `search_discovery_product_grid_insights`, `create_ranking_rule`, `create_discovery_experiment`, `start_discovery_experiment`; for Pattern 2 also `create_ranking_rule_variant`, `update_ranking_rule` |
| **Tested with** | Claude Code: the read-only steps (pre-flight checks, preview and sizing) were run against a demo account. **The writes are untested.** No rule or experiment was created; the write payloads were checked against the tool schemas only |
| **Maintainer** | Bloomreach |

## Example prompts

- "For 'mens belt', boost Tommy Hilfiger and Pacific and bury duplicate listings, but A/B test it first."
- "Set up an A/B test of a ranking rule for the dresses category."
- "I want to test pinning our new arrivals for 'sneakers' before rolling it out."

See [examples/mens-belt.md](examples/mens-belt.md) for a full example plan.

## Notes and limitations

- **Writes are untested.** In particular, it isn't confirmed whether `create_discovery_experiment` accepts a disabled rule. If it doesn't, the skill stops and explains the trade-off rather than enabling the rule on its own.
- `create_ranking_rule` defaults to `enabled: true` (live for everyone). The skill always sends `enabled: false`.
- A rule can't be previewed before it exists, so `scripts/simulate_rerank.py` gives an offline, strongest-case preview from the live grid. The real effect depends on the boost strength.
- `scripts/estimate_duration.py` estimates the test length. Both scripts use the Python standard library and make no network calls.
- Implicit invocation is turned off for OpenAI clients (`agents/openai.yaml`), because this skill writes.
- Use [discovery-experiment-readout](../discovery-experiment-readout/) to read the results.
