# Prediction activation check

Checks whether the predictive models in a Bloomreach Engagement project are earning their keep. It lists every prediction (churn, purchase propensity, lifetime value and similar), finds where each model's score is referenced across segmentations, customer filters, scenarios, email and SMS campaigns, web layers, aggregates, expressions, reports and dashboards, and classifies each model as activated, used only in reporting, used only by inactive flows, or unused. It flags models whose training or refresh looks stale or failing, and gives each unused model a concrete activation idea with a hand-off to the right skill. It reads definitions only and never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_predictions`, `get_customer_property_schema` (fallback), `search_segmentations`, `search_customer_filters`, `search_aggregates`, `search_running_aggregates`, `search_expressions`, `search_scenarios`, `search_scenario_nodes` (via `call_tool`), `search_email_campaigns`, `search_sms_campaigns`, `search_banners`, `search_reports`, `search_dashboards` |
| **Tested with** | Claude Code, read-only and metadata only: `list_cloud_organizations`, `list_projects`, `search_predictions` (list mode, on a sandbox and a production project: **both returned HTTP 403**), `search_segmentations` (list and one detail, on a sandbox, to confirm the customer filter shape and `used_by` prefixes), and `search_tools` (to confirm `search_scenario_nodes`). The reference-scanning script was run on illustrative inputs. **Because `search_predictions` was denied, the prediction detail fields (model type, output attribute, training status) and the shape of a prediction reference in a filter were not seen live**; the skill searches for the prediction ID and attribute name as plain strings so it doesn't depend on them. Not run end to end, and not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Are we actually using our predictive models?"
- "We built a churn prediction last year. Is anything using it?"
- "Which campaigns use our purchase propensity model?"
- "Find predictions that are built but not activated, and tell me what to do with them."

See [examples/illustrative-activation-check.md](examples/illustrative-activation-check.md) for an example output. Its names and numbers are illustrative.

## How it works

1. **Predictions:** lists them with `search_predictions`, then reads each one for its model type, target, output attribute and training settings. If the call returns HTTP 403, it explains the permission needed and falls back to likely prediction-output properties from the customer property schema, confirmed with the user.
2. **Refresh health:** flags models whose last training is older than twice their refresh interval (or 90 days), that show errors, or that have never been trained. If the API doesn't return training dates, it says so rather than guessing.
3. **References:** searches segmentations, customer filters, derived attributes, scenarios, campaigns, web layers, reports and dashboards for each model's ID and output attribute, following segmentations' `used_by` lists and derived attributes downstream. See [references/where-predictions-hide.md](references/where-predictions-hide.md). [scripts/find_prediction_refs.py](scripts/find_prediction_refs.py) does the matching over saved definitions (standard library only, no network).
4. **Classification and ideas:** activated, inactive use only, reporting only or unused, plus a stale flag, with one activation idea per model from [references/activation-playbook.md](references/activation-playbook.md).

It hands off to `winback-opportunity` (churn models), `engagement-segment-builder` (to build the audience), `campaign-planner` (to plan the sends) and `engagement-scenario-explainer` (to review a flow that already uses a model).

## Notes and limitations

- `search_predictions` returned HTTP 403 for every project tried in testing (October 2026). The account needs permission to view Predictions in Engagement. Without it, the skill runs in a clearly labelled fallback mode and can't judge refresh health.
- `search_sms_campaigns` can also return 403; the skill says the SMS check was skipped.
- Usage is judged from definitions, not from send or trigger history: an active scenario that references a model counts as activated even if few customers reach that branch.
- On large projects it checks the likeliest scenarios, campaigns and banners rather than every one, and says how many of each type it checked.
- It never reads individual customers' scores (`get_customer_prediction_score`), so it can't tell whether a score is actually filled. The activation playbook tells the user to check that before targeting.
