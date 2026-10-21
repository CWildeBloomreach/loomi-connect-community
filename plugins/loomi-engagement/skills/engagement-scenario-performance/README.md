# Engagement scenario performance

Shows how one Bloomreach Engagement scenario (automation flow) is doing, step by step: what each message or webhook sent, delivery, opens, clicks, bounces and unsubscribes, how many recipients bought soon afterwards, and how customers divided across each A/B split. It ends with the steps most worth fixing. It never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_scenarios`, `search_scenario_nodes`*, `estimate_eql_cost`, `execute_analytics_eql` (* found with `search_tools` and run with `call_tool` if not listed) |
| **Tested with** | Claude Code: the per-step status and "bought after" queries were run read-only against a demo project; the split-assignment query was run project-wide (by scenario, not by step) because the demo had no recent splits. Not yet tested in an OpenAI client |
| **Maintainer** | Bloomreach |

## Example prompts

- "How is our welcome series doing this month?"
- "Which step of the abandoned cart flow loses the most people?"
- "Does the win-back flow actually lead to purchases?"

See [examples/illustrative-readout.md](examples/illustrative-readout.md) for illustrative output.

## Notes and limitations

- Only steps that send something (email, SMS, push, webhooks and similar) record results. Conditions, waits and limits don't, so they're not in the table.
- "Bought within N days" counts customers who bought after receiving the message. It isn't proof the message caused it.
- For whether one A/B variant beat another, it hands off to `engagement-experiment-readout`.
- On large projects the per-step query rates as high cost for 90 days. It keeps periods short and never runs very-high-cost queries.
