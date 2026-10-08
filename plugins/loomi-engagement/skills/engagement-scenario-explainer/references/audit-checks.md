# Scenario audit checks

Apply these checks to each scenario. Use the smallest set of calls that answers each check. Report a finding only when the evidence supports it, and say what you didn't check.

## Severity

- **Action:** probably broken or wasteful now. Fix or archive it.
- **Review:** may be intended, but a person should confirm.
- **Info:** worth knowing, no action needed.

## From the scenario list alone (no extra calls)

| Check | Rule | Severity | Suggested action |
|---|---|---|---|
| Stale draft | `status` = `draft` and `edited` more than 90 days ago | Review | Archive it if it's no longer planned |
| Long-inactive | `status` = `inactive` or `paused` and `edited` more than 180 days ago | Review | Archive it, or note why it's kept |
| Old and active, untouched | `status` = `active` and `edited` more than 365 days ago | Info | Confirm the content and audience are still current |
| Paused by Bloomreach | appears with `paused_by_bloomreach=true` | Action | Find out why (often a sending or throughput issue) before restarting |
| Duplicate-looking names | names that differ only by "copy", "v2", "test", "template" | Review | Keep one source of truth |

Use 90 / 180 / 365 days as defaults, and change them if the user gives other thresholds.

## From the graph map (`search_scenario_nodes`, list mode)

| Check | Rule | Severity |
|---|---|---|
| No trigger | no node type ends in `-trigger` | Action |
| Only a manual trigger | the only triggers are `now-trigger` with `active: false` | Info (a one-off or manual flow) |
| Disconnected action | an action node (`send-*`, `push-*`, `*-webhook-action`, `set-property-action`, ...) with no incoming connections | Review: it never runs. Often a leftover old version |
| Orphan trigger | a trigger with no outgoing connections | Review |
| Dead-end condition | a `condition` whose outputs aren't connected | Review |
| A/B split with no branches | an `ab-split` with no outgoing connections | Info: often used only to assign holdout or test groups that other scenarios read. Confirm it's intended |
| No actions | active scenario with no action node on any connected path | Review |

`label` nodes never have connections, so never flag them.

## From node configuration and references

| Check | Rule | Severity |
|---|---|---|
| Missing segmentation | a filter atom with `attribute.type` = `segmentation` whose `id` isn't in the `search_segmentations` list (the list includes archived segmentations, flagged `archived: true`) | Action |
| Archived segmentation | the referenced segmentation has `archived: true` | Action |
| Missing aggregate / expression / prediction | the `id` isn't found by the matching search tool | Action |
| Missing template | `template_id` isn't null and isn't found by `search_email_assets` (check archived ones too) | Action |
| Unknown consent category | `consent_category` isn't in `get_consent_settings` → `categories[].id` | Action |
| Messages without consent | a message action with `general_consent: true` and no `consent_category` | Review: compliance |
| Hard-coded recipients | a webhook or condition that lists email addresses or user IDs in the configuration | Review: personal data in configuration, and hard to maintain. Don't repeat the addresses |
| Unverifiable reference | an ID with no matching read tool, such as limit-node steps or saved metrics in Jinja | Info: "not verified" |

## Run activity (optional, costly)

Scenario and campaign sends are tracked as the `campaign` event, with properties including `campaign_id` (the scenario ID) and `action_type`. To see which scenarios ran recently:

```
select count event campaign by event campaign.campaign_id grouping top 50 in last 30 days
```

- This query parsed successfully in testing. On a project with hundreds of millions of events, `estimate_eql_cost` rated it **high** even for a 1-day window, so it wasn't run. Always estimate first.
- Run it only if the estimate is `low` or `medium`, or if the user agrees to a `high` one. Never run `very_high`.
- Match the returned `campaign_id` values to scenario `_id`s. An **active** scenario with no `campaign` events in 30 days is an **Action** finding ("active but not running"). Check its trigger first: a yearly or date-based flow may simply not be due.
- If the project has no `campaign` event in `get_event_schema`, skip this check and say so.
