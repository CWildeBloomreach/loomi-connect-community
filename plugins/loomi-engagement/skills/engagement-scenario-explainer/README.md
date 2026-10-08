# Engagement scenario explainer

Explains a Bloomreach Engagement scenario (automation flow) in plain English: how customers enter, who qualifies, what happens step by step, and which channels and consent categories it uses. An audit mode checks every scenario in a project for stale drafts, long-inactive flows, disconnected nodes, and references to segmentations, templates or consent categories that no longer exist. It never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_scenarios`, `search_scenario_nodes`*, `search_segmentations`, `search_customer_filters`, `search_aggregates`, `search_expressions`, `search_predictions`, `search_email_campaigns`, `search_sms_campaigns`, `search_email_assets`*, `get_consent_settings`*, `estimate_eql_cost`, `execute_analytics_eql` (* found with `search_tools` and run with `call_tool`) |
| **Tested with** | Claude Code: live, read-only run of the method against a real project's scenario metadata (explain mode, and audit checks on a sample of scenarios). Run-activity EQL was parsed and cost-estimated but not executed. Not yet tested in an OpenAI client |
| **Maintainer** | Bloomreach |

## Example prompts

- "What does our cart abandonment scenario actually do?"
- "Explain the 'Welcome series' flow in plain English. Who gets it?"
- "Audit our scenarios. Which ones are stale or broken?"
- "Do any of our automations point at segments that don't exist any more?"

See [examples/explain-and-audit.md](examples/explain-and-audit.md) for illustrative output.

## Notes and limitations

- Scenario list records don't include triggers or run history, so the audit needs at least one call per scenario it inspects. For big projects it asks before opening more than about 20.
- "Last run" relies on an EQL count of the `campaign` event. On very large projects this rates as high cost even for short windows, so it's optional and needs the user's agreement.
- Some references, such as limit-node steps and saved metrics used in Jinja, have no read tool. They're reported as "not verified", not as broken.
- Webhook payloads and headers can contain personal data or tokens. The skill describes webhooks but never repeats their content.
- [scripts/scenario_graph.py](scripts/scenario_graph.py) (standard library, no network) summarises a saved scenario response: triggers, a flow outline, references and structural warnings.
