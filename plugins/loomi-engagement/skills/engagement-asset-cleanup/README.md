# Engagement asset cleanup

Builds a hygiene report for a whole Bloomreach Engagement project. It inventories scenarios, email and SMS campaigns, segmentations, event segmentations, aggregates, running aggregates, expressions, customer filters, reports, funnels, trends, dashboards and (optionally) catalogs and initiatives. It flags old drafts never launched, test copies ("copy of", test, tmp, old, dates in names), stopped or long-inactive scenarios, active scenarios that look stale, analytics objects nothing references, duplicate names, and items outside initiatives where filing is the convention. It returns a prioritised list grouped by asset type, with an **archive / delete / review with owner** suggestion and a summary count. It never changes anything.

Web layers, in-app messages, surveys and experiments are covered by [onsite-experience-audit](../onsite-experience-audit/), and per-scenario structural checks by [engagement-scenario-explainer](../engagement-scenario-explainer/).

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_scenarios`, `search_email_campaigns`, `search_sms_campaigns`, `search_segmentations`, `search_event_segmentations`, `search_aggregates`, `search_running_aggregates`, `search_expressions`, `search_customer_filters`, `search_reports`, `search_funnels`, `search_trends`, `search_dashboards`, `search_initiatives`, `get_initiative_items`*, optionally `search_catalogs`, `get_catalog_usages`, `get_campaign_calendar`, `get_event_schema`, `estimate_eql_cost`, `execute_analytics_eql` (* found with `search_tools` and run with `call_tool`) |
| **Tested with** | Claude Code: list calls run live and read-only against a sandbox project for `search_scenarios`, `search_segmentations`, `search_aggregates`, `search_running_aggregates`, `search_expressions`, `search_customer_filters`, `search_reports`, `search_dashboards` and `search_initiatives`; `search_email_campaigns` returned HTTP 403, so the campaign checks are untested live. `search_sms_campaigns`, `search_event_segmentations`, `search_funnels`, `search_trends`, `search_catalogs`, `get_catalog_usages`, `get_initiative_items`, `get_campaign_calendar` and the activity EQL were checked by schema only, not run. The sandbox was small (one scenario), so pagination and capping weren't exercised. The script was tested on synthetic responses. Not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Our Engagement project is a mess. What can we clean up?"
- "Find unused segments and aggregates."
- "List old draft scenarios and test copies we should archive."
- "Are there duplicate campaigns or reports?"

See [examples/illustrative-cleanup.md](examples/illustrative-cleanup.md) for an example output. Its names and numbers are illustrative.

## How it works

1. Lists each asset type once (list calls only, one at a time), paginating scenarios and email campaigns and capping at 1,000 per type.
2. Applies the checks in [references/cleanup-checks.md](references/cleanup-checks.md): drafts and stopped items by status and last-edited date, test copies and dated names by pattern, unreferenced analytics objects by their `used_by` list, duplicates by normalised name, and filing by `initiative_id`. [scripts/cleanup_inventory.py](scripts/cleanup_inventory.py) does this from saved responses (standard library only, no network, never prints editor names).
3. Optionally checks whether active scenarios still send, using the campaign calendar or a cost-estimated EQL count of the `campaign` event.
4. Prioritises and suggests archive, delete or review with owner, preferring archive when in doubt.

## Notes and limitations

- **Usage checks are partial.** Segmentations and aggregates carry a `used_by` list; expressions, customer filters, reports, funnels, trends and dashboards don't, so the skill doesn't call those unused. `used_by` also misses references from Jinja in templates, exports, integrations and API consumers, so "unreferenced" is a review, not a delete.
- Scenario lists have no run history. "Never ran" is inferred from `draft` status; "active but quiet" needs the optional EQL check.
- `search_email_campaigns` and `search_sms_campaigns` can return HTTP 403 depending on permissions; the report says "not checked" for them.
- Item collections are a Data Hub object (workspace-scoped), so the skill covers Engagement catalogs instead, via `search_catalogs` and `get_catalog_usages`.
- Lists include editor names; the report never repeats them.
